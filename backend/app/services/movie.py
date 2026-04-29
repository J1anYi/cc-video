from typing import Optional, List as TypingList
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, PublicationStatus
from app.schemas.movie import MovieCreate, MovieUpdate


class MovieService:
    """Service layer for movie CRUD operations."""

    async def create(
        self, db: AsyncSession, movie_data: MovieCreate
    ) -> Movie:
        """Create a new movie record.

        Args:
            db: Database session
            movie_data: Movie creation data

        Returns:
            Created movie with generated ID
        """
        movie = Movie(
            title=movie_data.title,
            description=movie_data.description,
            publication_status=movie_data.publication_status,
        )
        db.add(movie)
        await db.commit()
        await db.refresh(movie)
        return movie

    async def get_by_id(
        self, db: AsyncSession, movie_id: int
    ) -> Optional[Movie]:
        """Get a movie by ID.

        Args:
            db: Database session
            movie_id: Movie ID to look up

        Returns:
            Movie if found, None otherwise
        """
        result = await db.execute(select(Movie).where(Movie.id == movie_id))
        return result.scalar_one_or_none()

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> TypingList[Movie]:
        """Get all movies (for admin view, includes unpublished).

        Args:
            db: Database session
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of all movies
        """
        result = await db.execute(select(Movie).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_published(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> TypingList[Movie]:
        """Get only published movies (for user view).

        Args:
            db: Database session
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return

        Returns:
            List of published movies
        """
        result = await db.execute(
            select(Movie)
            .where(Movie.publication_status == PublicationStatus.PUBLISHED)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(
        self, db: AsyncSession, movie_id: int, movie_data: MovieUpdate
    ) -> Optional[Movie]:
        """Update a movie with partial update support.

        Only updates fields that are provided (not None).

        Args:
            db: Database session
            movie_id: Movie ID to update
            movie_data: Partial movie update data

        Returns:
            Updated movie if found, None otherwise
        """
        movie = await self.get_by_id(db, movie_id)
        if not movie:
            return None

        update_data = movie_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(movie, field, value)

        await db.commit()
        await db.refresh(movie)
        return movie

    async def delete(self, db: AsyncSession, movie_id: int) -> bool:
        """Hard delete a movie.

        Args:
            db: Database session
            movie_id: Movie ID to delete

        Returns:
            True if deleted, False if not found
        """
        movie = await self.get_by_id(db, movie_id)
        if not movie:
            return False

        await db.delete(movie)
        await db.commit()
        return True


movie_service = MovieService()
