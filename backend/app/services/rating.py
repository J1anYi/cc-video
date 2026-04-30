from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rating import Rating
from app.models.activity import ActivityType
from app.schemas.rating import RatingCreate, RatingUpdate, MovieRatingStats
from app.services.activity import activity_service

class RatingService:
    @staticmethod
    async def create_or_update_rating(db: AsyncSession, user_id: int, movie_id: int, rating_data: RatingCreate) -> Rating:
        result = await db.execute(
            select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.rating = rating_data.rating
            await db.commit()
            await db.refresh(existing)
            return existing
        rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating_data.rating)
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        # Create activity for new rating
        await activity_service.create_activity(
            db, user_id, ActivityType.RATING_ADDED.value, movie_id=movie_id, reference_id=rating.id
        )
        return rating

    @staticmethod
    async def get_user_rating(db: AsyncSession, user_id: int, movie_id: int):
        result = await db.execute(
            select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_movie_rating_stats(db: AsyncSession, movie_id: int, user_id: int | None = None) -> MovieRatingStats:
        result = await db.execute(
            select(func.avg(Rating.rating), func.count(Rating.id)).where(Rating.movie_id == movie_id)
        )
        avg_rating, count = result.one()
        user_rating = None
        if user_id:
            user_result = await db.execute(
                select(Rating.rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
            )
            user_rating = user_result.scalar_one_or_none()
        return MovieRatingStats(
            average_rating=round(avg_rating, 1) if avg_rating else None,
            rating_count=count or 0,
            user_rating=user_rating
        )

    @staticmethod
    async def delete_rating(db: AsyncSession, user_id: int, movie_id: int) -> bool:
        result = await db.execute(
            select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
        )
        rating = result.scalar_one_or_none()
        if rating:
            await db.delete(rating)
            await db.commit()
            return True
        return False

rating_service = RatingService()
