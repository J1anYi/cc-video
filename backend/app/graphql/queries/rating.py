import strawberry
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from strawberry.types import Info

from app.models.rating import Rating
from app.graphql.types import RatingType


@strawberry.type
class RatingQuery:
    @strawberry.field
    async def rating(self, info: Info, rating_id: int) -> Optional[RatingType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(Rating).where(Rating.id == rating_id))
        rating = result.scalar_one_or_none()
        if not rating:
            return None
        return RatingType(
            id=rating.id,
            user_id=rating.user_id,
            movie_id=rating.movie_id,
            rating=rating.rating,
            created_at=rating.created_at,
            updated_at=rating.updated_at,
        )

    @strawberry.field
    async def ratings(
        self, info: Info, movie_id: Optional[int] = None, limit: int = 10, offset: int = 0
    ) -> List[RatingType]:
        db: AsyncSession = info.context["db"]
        query = select(Rating)
        if movie_id:
            query = query.where(Rating.movie_id == movie_id)
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        ratings = result.scalars().all()
        return [
            RatingType(
                id=r.id,
                user_id=r.user_id,
                movie_id=r.movie_id,
                rating=r.rating,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in ratings
        ]

    @strawberry.field
    async def user_ratings(self, info: Info, user_id: int, limit: int = 10) -> List[RatingType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Rating).where(Rating.user_id == user_id).limit(limit)
        )
        ratings = result.scalars().all()
        return [
            RatingType(
                id=r.id,
                user_id=r.user_id,
                movie_id=r.movie_id,
                rating=r.rating,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in ratings
        ]
