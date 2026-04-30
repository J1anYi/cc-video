import strawberry
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from strawberry.types import Info

from app.models.movie import Movie
from app.models.rating import Rating
from app.models.review import Review
from app.graphql.types import MovieType, MovieDetail, MovieFilterInput


@strawberry.type
class MovieQuery:
    @strawberry.field
    async def movie(self, info: Info, movie_id: int) -> Optional[MovieType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        if not movie:
            return None
        return MovieType(
            id=movie.id,
            title=movie.title,
            description=movie.description,
            release_year=movie.release_year,
            duration_minutes=movie.duration_minutes,
            genre=movie.genre,
            poster_url=movie.poster_url,
            video_url=movie.video_url,
            average_rating=movie.average_rating,
            created_at=movie.created_at,
            updated_at=movie.updated_at,
        )

    @strawberry.field
    async def movies(
        self, info: Info, limit: int = 10, offset: int = 0, filter: Optional[MovieFilterInput] = None
    ) -> List[MovieType]:
        db: AsyncSession = info.context["db"]
        query = select(Movie)

        if filter:
            if filter.genre:
                query = query.where(Movie.genre == filter.genre)
            if filter.year_from:
                query = query.where(Movie.release_year >= filter.year_from)
            if filter.year_to:
                query = query.where(Movie.release_year <= filter.year_to)
            if filter.min_rating:
                query = query.where(Movie.average_rating >= filter.min_rating)
            if filter.search:
                query = query.where(Movie.title.ilike(f"%{filter.search}%"))

        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        movies = result.scalars().all()

        return [
            MovieType(
                id=m.id,
                title=m.title,
                description=m.description,
                release_year=m.release_year,
                duration_minutes=m.duration_minutes,
                genre=m.genre,
                poster_url=m.poster_url,
                video_url=m.video_url,
                average_rating=m.average_rating,
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in movies
        ]

    @strawberry.field
    async def movie_detail(self, info: Info, movie_id: int) -> Optional[MovieDetail]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalar_one_or_none()
        if not movie:
            return None

        ratings_count = await db.execute(
            select(func.count()).where(Rating.movie_id == movie_id)
        )
        reviews_count = await db.execute(
            select(func.count()).where(Review.movie_id == movie_id)
        )

        return MovieDetail(
            movie=MovieType(
                id=movie.id,
                title=movie.title,
                description=movie.description,
                release_year=movie.release_year,
                duration_minutes=movie.duration_minutes,
                genre=movie.genre,
                poster_url=movie.poster_url,
                video_url=movie.video_url,
                average_rating=movie.average_rating,
                created_at=movie.created_at,
                updated_at=movie.updated_at,
            ),
            ratings_count=ratings_count.scalar() or 0,
            reviews_count=reviews_count.scalar() or 0,
        )

    @strawberry.field
    async def search_movies(self, info: Info, query: str, limit: int = 10) -> List[MovieType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Movie).where(Movie.title.ilike(f"%{query}%")).limit(limit)
        )
        movies = result.scalars().all()
        return [
            MovieType(
                id=m.id,
                title=m.title,
                description=m.description,
                release_year=m.release_year,
                duration_minutes=m.duration_minutes,
                genre=m.genre,
                poster_url=m.poster_url,
                video_url=m.video_url,
                average_rating=m.average_rating,
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in movies
        ]
