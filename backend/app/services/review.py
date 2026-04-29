from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review
from app.models.user import User
from app.models.activity import ActivityType
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.services.activity import activity_service

class ReviewService:
    @staticmethod
    async def create_review(db: AsyncSession, user_id: int, movie_id: int, review_data: ReviewCreate) -> Review:
        review = Review(user_id=user_id, movie_id=movie_id, content=review_data.content)
        db.add(review)
        await db.commit()
        await db.refresh(review)
        # Create activity for new review
        await activity_service.create_activity(
            db, user_id, ActivityType.REVIEW_POSTED.value, movie_id=movie_id, reference_id=review.id
        )
        return review

    @staticmethod
    async def update_review(db: AsyncSession, user_id: int, review_id: int, review_data: ReviewUpdate):
        result = await db.execute(
            select(Review).where(Review.id == review_id, Review.user_id == user_id)
        )
        review = result.scalar_one_or_none()
        if review:
            review.content = review_data.content
            await db.commit()
            await db.refresh(review)
        return review

    @staticmethod
    async def get_movie_reviews(db: AsyncSession, movie_id: int, skip: int = 0, limit: int = 20):
        result = await db.execute(
            select(Review, User).join(User).where(Review.movie_id == movie_id).order_by(Review.created_at.desc()).offset(skip).limit(limit)
        )
        rows = result.all()
        reviews = []
        for review, user in rows:
            reviews.append(ReviewResponse(
                id=review.id,
                user_id=review.user_id,
                movie_id=review.movie_id,
                username=user.display_name or user.email,
                content=review.content,
                created_at=review.created_at,
                updated_at=review.updated_at
            ))
        count_result = await db.execute(select(func.count(Review.id)).where(Review.movie_id == movie_id))
        total = count_result.scalar()
        return reviews, total

    @staticmethod
    async def delete_review(db: AsyncSession, user_id: int, review_id: int) -> bool:
        result = await db.execute(select(Review).where(Review.id == review_id, Review.user_id == user_id))
        review = result.scalar_one_or_none()
        if review:
            await db.delete(review)
            await db.commit()
            return True
        return False

review_service = ReviewService()
