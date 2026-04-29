from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.models.user import User
from app.models.review import Review
from app.models.notification import NotificationType
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.notification import notification_service

class CommentService:
    @staticmethod
    async def create_comment(db: AsyncSession, user_id: int, review_id: int, comment_data: CommentCreate) -> Comment:
        comment = Comment(user_id=user_id, review_id=review_id, content=comment_data.content)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)

        # Notify review author about the comment
        review_result = await db.execute(select(Review).where(Review.id == review_id))
        review = review_result.scalar_one_or_none()
        if review and review.user_id != user_id:
            user_result = await db.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()
            commenter_name = user.display_name or user.email if user else "Someone"
            await notification_service.create_notification(
                db,
                user_id=review.user_id,
                notification_type=NotificationType.COMMENT_REPLY.value,
                title=f"{commenter_name} replied to your review",
                content=comment_data.content[:100] if len(comment_data.content) > 100 else comment_data.content,
                actor_id=user_id,
                target_type="comment",
                target_id=comment.id,
            )

        return comment

    @staticmethod
    async def get_review_comments(db: AsyncSession, review_id: int, skip: int = 0, limit: int = 20):
        result = await db.execute(
            select(Comment, User).join(User).where(Comment.review_id == review_id)
            .order_by(Comment.created_at.asc()).offset(skip).limit(limit)
        )
        rows = result.all()
        comments = []
        for comment, user in rows:
            comments.append(CommentResponse(
                id=comment.id,
                user_id=comment.user_id,
                review_id=comment.review_id,
                username=user.display_name or user.email,
                content=comment.content,
                created_at=comment.created_at
            ))
        count_result = await db.execute(select(func.count(Comment.id)).where(Comment.review_id == review_id))
        total = count_result.scalar()
        return comments, total

    @staticmethod
    async def delete_comment(db: AsyncSession, user_id: int, comment_id: int) -> bool:
        result = await db.execute(select(Comment).where(Comment.id == comment_id, Comment.user_id == user_id))
        comment = result.scalar_one_or_none()
        if comment:
            await db.delete(comment)
            await db.commit()
            return True
        return False

comment_service = CommentService()
