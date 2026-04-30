import strawberry
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from strawberry.types import Info

from app.models.review import Review
from app.graphql.types import ReviewType, ReviewCreateInput, ReviewUpdateInput


@strawberry.type
class ReviewMutation:
    @strawberry.mutation
    async def create_review(self, info: Info, input: ReviewCreateInput) -> Optional[ReviewType]:
        user = info.context.get("user")
        if not user:
            return None
        
        db: AsyncSession = info.context["db"]
        review = Review(
            user_id=user.id,
            movie_id=input.movie_id,
            content=input.content,
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)
        
        return ReviewType(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    @strawberry.mutation
    async def update_review(self, info: Info, review_id: int, input: ReviewUpdateInput) -> Optional[ReviewType]:
        user = info.context.get("user")
        if not user:
            return None
        
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Review).where(Review.id == review_id, Review.user_id == user.id)
        )
        review = result.scalar_one_or_none()
        
        if not review:
            return None
        
        review.content = input.content
        review.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(review)
        
        return ReviewType(
            id=review.id,
            user_id=review.user_id,
            movie_id=review.movie_id,
            content=review.content,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    @strawberry.mutation
    async def delete_review(self, info: Info, review_id: int) -> bool:
        user = info.context.get("user")
        if not user:
            return False
        
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Review).where(Review.id == review_id, Review.user_id == user.id)
        )
        review = result.scalar_one_or_none()
        
        if not review:
            return False
        
        await db.delete(review)
        await db.commit()
        return True
