import strawberry
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from strawberry.types import Info

from app.models.review import Review
from app.graphql.types import ReviewType


@strawberry.type
class ReviewQuery:
    @strawberry.field
    async def review(self, info: Info, review_id: int) -> Optional[ReviewType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(Review).where(Review.id == review_id))
        review = result.scalar_one_or_none()
        if not review:
            return None
        return ReviewType(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    @strawberry.field
    async def reviews(
        self, info: Info, movie_id: Optional[int] = None, limit: int = 10, offset: int = 0
    ) -> List[ReviewType]:
        db: AsyncSession = info.context["db"]
        query = select(Review)
        if movie_id:
            query = query.where(Review.movie_id == movie_id)
        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        reviews = result.scalars().all()
        return [
            ReviewType(
                id=r.id,
                user_id=r.user_id,
                movie_id=r.movie_id,
                content=r.content,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in reviews
        ]

    @strawberry.field
    async def user_reviews(self, info: Info, user_id: int, limit: int = 10) -> List[ReviewType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Review).where(Review.user_id == user_id).limit(limit)
        )
        reviews = result.scalars().all()
        return [
            ReviewType(
                id=r.id,
                user_id=r.user_id,
                movie_id=r.movie_id,
                content=r.content,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in reviews
        ]
