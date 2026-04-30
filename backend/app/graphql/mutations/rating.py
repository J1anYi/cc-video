import strawberry
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from strawberry.types import Info

from app.models.rating import Rating
from app.graphql.types import RatingType, RatingCreateInput, RatingUpdateInput


@strawberry.type
class RatingMutation:
    @strawberry.mutation
    async def create_rating(self, info: Info, input: RatingCreateInput) -> Optional[RatingType]:
        user = info.context.get("user")
        if not user:
            return None
        
        db: AsyncSession = info.context["db"]
        rating = Rating(
            user_id=user.id,
            movie_id=input.movie_id,
            rating=input.rating,
        )
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        
        return RatingType(
            id=rating.id,
            user_id=rating.user_id,
            movie_id=rating.movie_id,
            rating=rating.rating,
            created_at=rating.created_at,
            updated_at=rating.updated_at,
        )

    @strawberry.mutation
    async def update_rating(self, info: Info, rating_id: int, input: RatingUpdateInput) -> Optional[RatingType]:
        user = info.context.get("user")
        if not user:
            return None
        
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Rating).where(Rating.id == rating_id, Rating.user_id == user.id)
        )
        rating = result.scalar_one_or_none()
        
        if not rating:
            return None
        
        rating.rating = input.rating
        rating.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(rating)
        
        return RatingType(
            id=rating.id,
            user_id=rating.user_id,
            movie_id=rating.movie_id,
            rating=rating.rating,
            created_at=rating.created_at,
            updated_at=rating.updated_at,
        )

    @strawberry.mutation
    async def delete_rating(self, info: Info, rating_id: int) -> bool:
        user = info.context.get("user")
        if not user:
            return False
        
        db: AsyncSession = info.context["db"]
        result = await db.execute(
            select(Rating).where(Rating.id == rating_id, Rating.user_id == user.id)
        )
        rating = result.scalar_one_or_none()
        
        if not rating:
            return False
        
        await db.delete(rating)
        await db.commit()
        return True
