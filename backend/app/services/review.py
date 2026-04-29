from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review
from app.models.user import User
from app.models.activity import ActivityType
from app.models.notification import NotificationType
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.services.activity import activity_service
from app.services.notification import notification_service
from app.services.follow import follow_service
from app.services.movie import movie_service

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

        # Notify followers about the new review
        follower_ids = await follow_service.get_follower_ids(db, user_id)
        movie = await movie_service.get_by_id(db, movie_id)
        movie_title = movie.title if movie else "a movie"
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        user_name = user.display_name or user.email if user else "Someone"

        for follower_id in follower_ids:
            await notification_service.create_notification(
                db,
                user_id=follower_id,
                notification_type=NotificationType.NEW_REVIEW.value,
                title=f"{user_name} posted a new review",
                content=f"{user_name} reviewed {movie_title}",
                actor_id=user_id,
                target_type="review",
                target_id=review.id,
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
