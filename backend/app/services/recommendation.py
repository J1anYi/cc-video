from datetime import datetime
from typing import List, Tuple
from collections import Counter
from sqlalchemy import select, and_, not_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.watch_history import WatchHistory
from app.models.favorite import Favorite
from app.models.movie import Movie, PublicationStatus
from app.schemas.recommendation import (
    RecommendedMovie,
    ContinueWatchingItem,
)


class RecommendationService:
    async def get_personalized_recommendations(
        self, db: AsyncSession, user_id: int, limit: int = 10
    ) -> List[RecommendedMovie]:
        """
        Get personalized movie recommendations based on watch history and favorites.
        Uses content-based filtering with category matching.
        """
        # Get all movies user has already watched (for exclusion)
        watched_result = await db.execute(
            select(WatchHistory.movie_id).where(WatchHistory.user_id == user_id)
        )
        watched_ids = [row[0] for row in watched_result.fetchall()]

        # Get categories from watched movies (weight: 1)
        watched_movies_result = await db.execute(
            select(Movie.category).where(Movie.id.in_(watched_ids))
        )
        watched_categories = [row[0] for row in watched_movies_result.fetchall() if row[0]]

        # Get categories from favorites (weight: 2)
        favorites_result = await db.execute(
            select(Movie.category)
            .join(Favorite, Favorite.movie_id == Movie.id)
            .where(Favorite.user_id == user_id)
        )
        favorite_categories = [row[0] for row in favorites_result.fetchall() if row[0]]

        # Score categories (favorites count 2x)
        category_scores = Counter()
        for cat in watched_categories:
            category_scores[cat] += 1
        for cat in favorite_categories:
            category_scores[cat] += 2  # Favorites weighted higher

        if not category_scores:
            # No preferences yet - return popular movies
            return await self._get_popular_movies(db, watched_ids, limit)

        # Get top categories (up to 3)
        top_categories = [cat for cat, _ in category_scores.most_common(3)]

        # Find movies in those categories
        result = await db.execute(
            select(Movie)
            .where(
                and_(
                    Movie.category.in_(top_categories),
                    Movie.publication_status == PublicationStatus.PUBLISHED,
                    not_(Movie.id.in_(watched_ids)) if watched_ids else True,
                )
            )
            .order_by(func.random())
            .limit(limit)
        )
        movies = result.scalars().all()

        # Build recommendations with reasons
        recommendations = []
        for movie in movies:
            if movie.category in favorite_categories:
                reason = f"Because you favorited {movie.category} movies"
            else:
                reason = f"Because you watched {movie.category} movies"
            recommendations.append(
                RecommendedMovie(movie=MovieResponse.model_validate(movie), reason=reason)
            )

        return recommendations

    async def _get_popular_movies(
        self, db: AsyncSession, exclude_ids: List[int], limit: int
    ) -> List[RecommendedMovie]:
        """Fallback: Get random popular movies when no preferences exist."""
        result = await db.execute(
            select(Movie)
            .where(
                and_(
                    Movie.publication_status == PublicationStatus.PUBLISHED,
                    not_(Movie.id.in_(exclude_ids)) if exclude_ids else True,
                )
            )
            .order_by(func.random())
            .limit(limit)
        )
        movies = result.scalars().all()

        from app.schemas.movie import MovieResponse
        return [
            RecommendedMovie(
                movie=MovieResponse.model_validate(movie),
                reason="Popular on CC Video"
            )
            for movie in movies
        ]

    async def get_continue_watching(
        self, db: AsyncSession, user_id: int, limit: int = 10
    ) -> List[ContinueWatchingItem]:
        """
        Get movies the user hasn't finished watching.
        Returns entries with progress < 100, sorted by most recent.
        """
        result = await db.execute(
            select(WatchHistory)
            .options(selectinload(WatchHistory.movie))
            .where(
                and_(
                    WatchHistory.user_id == user_id,
                    WatchHistory.progress < 100,
                )
            )
            .order_by(WatchHistory.last_watched_at.desc())
            .limit(limit)
        )
        entries = result.scalars().all()

        from app.schemas.movie import MovieResponse
        return [
            ContinueWatchingItem(
                movie=MovieResponse.model_validate(entry.movie),
                progress=entry.progress,
                last_watched_at=entry.last_watched_at.isoformat(),
            )
            for entry in entries
        ]


recommendation_service = RecommendationService()

# Import MovieResponse at the end to avoid circular import
from app.schemas.movie import MovieResponse
