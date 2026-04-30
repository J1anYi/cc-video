from datetime import datetime, timedelta
from typing import List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.watch_history import WatchHistory
from app.models.movie import Movie, PublicationStatus
from app.schemas.trending import TrendingMovie
from app.schemas.movie import MovieResponse


class TrendingService:
    async def get_trending_movies(
        self, db: AsyncSession, limit: int = 10
    ) -> List[TrendingMovie]:
        """Get trending movies based on watch count in last 7 days."""
        seven_days_ago = datetime.utcnow() - timedelta(days=7)

        # Count watches per movie in last 7 days
        result = await db.execute(
            select(WatchHistory.movie_id, func.count().label('count'))
            .where(WatchHistory.last_watched_at >= seven_days_ago)
            .group_by(WatchHistory.movie_id)
            .order_by(func.count().desc())
            .limit(limit)
        )
        movie_counts = result.fetchall()

        if not movie_counts:
            return []

        # Fetch movie details
        movie_ids = [row[0] for row in movie_counts]
        movies_result = await db.execute(
            select(Movie)
            .where(Movie.id.in_(movie_ids))
            .where(Movie.publication_status == PublicationStatus.PUBLISHED)
        )
        movies = {m.id: m for m in movies_result.scalars().all()}

        # Build response
        trending = []
        for movie_id, count in movie_counts:
            if movie_id in movies:
                trending.append(TrendingMovie(
                    movie=MovieResponse.model_validate(movies[movie_id]),
                    view_count=count
                ))
        return trending

    async def get_related_movies(
        self, db: AsyncSession, movie_id: int, limit: int = 4
    ) -> List[MovieResponse]:
        """Get related movies by same category."""
        # Get the current movie's category
        current_result = await db.execute(
            select(Movie).where(Movie.id == movie_id)
        )
        current_movie = current_result.scalar_one_or_none()

        if not current_movie or not current_movie.category:
            return []

        # Find movies with same category
        result = await db.execute(
            select(Movie)
            .where(
                and_(
                    Movie.category == current_movie.category,
                    Movie.id != movie_id,
                    Movie.publication_status == PublicationStatus.PUBLISHED
                )
            )
            .limit(limit)
        )
        movies = result.scalars().all()

        return [MovieResponse.model_validate(m) for m in movies]


trending_service = TrendingService()
