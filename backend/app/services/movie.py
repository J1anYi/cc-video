from typing import Optional, List as TypingList
from sqlalchemy import select, func, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.movie import Movie, PublicationStatus
from app.schemas.movie import MovieCreate, MovieUpdate


class MovieService:
    """Service layer for movie CRUD operations."""

    async def create(
        self, db: AsyncSession, movie_data: MovieCreate
    ) -> Movie:
        """Create a new movie record."""
        movie = Movie(
            title=movie_data.title,
            description=movie_data.description,
            category=movie_data.category,
            release_year=movie_data.release_year,
            duration_minutes=movie_data.duration_minutes,
            publication_status=movie_data.publication_status,
        )
        db.add(movie)
        await db.commit()
        await db.refresh(movie)
        return movie

    async def get_by_id(
        self, db: AsyncSession, movie_id: int
    ) -> Optional[Movie]:
        """Get a movie by ID."""
        result = await db.execute(select(Movie).where(Movie.id == movie_id))
        return result.scalar_one_or_none()

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> TypingList[Movie]:
        """Get all movies (for admin view, includes unpublished)."""
        result = await db.execute(select(Movie).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_published(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> TypingList[Movie]:
        """Get only published movies (for user view)."""
        result = await db.execute(
            select(Movie)
            .where(Movie.publication_status == PublicationStatus.PUBLISHED)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_published_filtered(
        self,
        db: AsyncSession,
        search: Optional[str] = None,
        category: Optional[str] = None,
        min_rating: Optional[float] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        duration_from: Optional[int] = None,
        duration_to: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> TypingList[Movie]:
        """Get published movies with advanced filtering."""
        query = select(Movie).where(
            Movie.publication_status == PublicationStatus.PUBLISHED
        )

        if search:
            query = query.where(Movie.title.ilike(f"%{search}%"))

        if category:
            query = query.where(Movie.category == category)

        if year_from:
            query = query.where(Movie.release_year >= year_from)

        if year_to:
            query = query.where(Movie.release_year <= year_to)

        if duration_from:
            query = query.where(Movie.duration_minutes >= duration_from)

        if duration_to:
            query = query.where(Movie.duration_minutes <= duration_to)

        # Handle sorting
        sort_column = Movie.created_at
        if sort_by == "title":
            sort_column = Movie.title
        elif sort_by == "year":
            sort_column = Movie.release_year
        elif sort_by == "rating":
            sort_column = Movie.created_at
        elif sort_by == "created_at":
            sort_column = Movie.created_at

        if sort_order == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def count_published_filtered(
        self,
        db: AsyncSession,
        search: Optional[str] = None,
        category: Optional[str] = None,
        min_rating: Optional[float] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        duration_from: Optional[int] = None,
        duration_to: Optional[int] = None,
    ) -> int:
        """Count published movies with advanced filtering."""
        query = select(func.count(Movie.id)).where(
            Movie.publication_status == PublicationStatus.PUBLISHED
        )

        if search:
            query = query.where(Movie.title.ilike(f"%{search}%"))

        if category:
            query = query.where(Movie.category == category)

        if year_from:
            query = query.where(Movie.release_year >= year_from)

        if year_to:
            query = query.where(Movie.release_year <= year_to)

        if duration_from:
            query = query.where(Movie.duration_minutes >= duration_from)

        if duration_to:
            query = query.where(Movie.duration_minutes <= duration_to)

        result = await db.execute(query)
        return result.scalar() or 0

    async def get_categories(self, db: AsyncSession) -> TypingList[str]:
        """Get list of distinct categories from published movies."""
        query = (
            select(Movie.category)
            .where(
                Movie.publication_status == PublicationStatus.PUBLISHED,
                Movie.category.isnot(None)
            )
            .distinct()
        )

        result = await db.execute(query)
        return [cat for cat in result.scalars().all() if cat]

    async def update(
        self, db: AsyncSession, movie_id: int, movie_data: MovieUpdate
    ) -> Optional[Movie]:
        """Update a movie with partial update support."""
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
        """Hard delete a movie."""
        movie = await self.get_by_id(db, movie_id)
        if not movie:
            return False

        await db.delete(movie)
        await db.commit()
        return True


movie_service = MovieService()
