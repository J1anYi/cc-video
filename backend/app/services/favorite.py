from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.favorite import Favorite
from app.models.movie import Movie


class FavoriteService:
    async def get_user_favorites(self, db: AsyncSession, user_id: int) -> List[Favorite]:
        """Get user's favorites sorted by most recent first."""
        result = await db.execute(
            select(Favorite)
            .options(selectinload(Favorite.movie))
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )
        return list(result.scalars().all())

    async def add_favorite(self, db: AsyncSession, user_id: int, movie_id: int) -> Favorite:
        """Add a movie to favorites."""
        # Check if already exists
        existing = await self.get_favorite_entry(db, user_id, movie_id)
        if existing:
            return existing

        favorite = Favorite(
            user_id=user_id,
            movie_id=movie_id,
            created_at=datetime.utcnow(),
        )
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite

    async def remove_favorite(self, db: AsyncSession, user_id: int, movie_id: int) -> bool:
        """Remove a movie from favorites."""
        result = await db.execute(
            select(Favorite).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.movie_id == movie_id
                )
            )
        )
        favorite = result.scalar_one_or_none()
        if favorite:
            await db.delete(favorite)
            await db.commit()
            return True
        return False

    async def get_favorite_entry(
        self, db: AsyncSession, user_id: int, movie_id: int
    ) -> Optional[Favorite]:
        """Get a single favorite entry for a specific movie."""
        result = await db.execute(
            select(Favorite)
            .options(selectinload(Favorite.movie))
            .where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.movie_id == movie_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def is_favorite(self, db: AsyncSession, user_id: int, movie_id: int) -> bool:
        """Check if a movie is in user's favorites."""
        result = await db.execute(
            select(Favorite.id).where(
                and_(
                    Favorite.user_id == user_id,
                    Favorite.movie_id == movie_id
                )
            )
        )
        return result.scalar_one_or_none() is not None


favorite_service = FavoriteService()
