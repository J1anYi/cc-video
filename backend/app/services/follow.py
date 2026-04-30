from datetime import datetime
from typing import List
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user_follow import UserFollow
from app.models.user import User
from app.models.notification import NotificationType
from app.services.notification import notification_service


class FollowService:
    async def follow_user(self, db: AsyncSession, follower_id: int, following_id: int) -> UserFollow:
        """Follow a user."""
        # Prevent self-following
        if follower_id == following_id:
            raise ValueError("Cannot follow yourself")

        # Check if already following
        existing = await self.get_follow(db, follower_id, following_id)
        if existing:
            return existing

        follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id,
            created_at=datetime.utcnow(),
        )
        db.add(follow)
        await db.commit()
        await db.refresh(follow)

        # Notify the followed user
        follower_result = await db.execute(select(User).where(User.id == follower_id))
        follower = follower_result.scalar_one_or_none()
        follower_name = follower.display_name or follower.email if follower else "Someone"

        await notification_service.create_notification(
            db,
            user_id=following_id,
            notification_type=NotificationType.NEW_FOLLOWER.value,
            title=f"{follower_name} started following you",
            content=None,
            actor_id=follower_id,
            target_type="user",
            target_id=follower_id,
        )

        return follow

    async def unfollow_user(self, db: AsyncSession, follower_id: int, following_id: int) -> bool:
        """Unfollow a user."""
        result = await db.execute(
            select(UserFollow).where(
                and_(
                    UserFollow.follower_id == follower_id,
                    UserFollow.following_id == following_id
                )
            )
        )
        follow = result.scalar_one_or_none()
        if follow:
            await db.delete(follow)
            await db.commit()
            return True
        return False

    async def get_follow(self, db: AsyncSession, follower_id: int, following_id: int) -> UserFollow | None:
        """Get a follow relationship."""
        result = await db.execute(
            select(UserFollow).where(
                and_(
                    UserFollow.follower_id == follower_id,
                    UserFollow.following_id == following_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def is_following(self, db: AsyncSession, follower_id: int, following_id: int) -> bool:
        """Check if user is following another user."""
        result = await db.execute(
            select(UserFollow.id).where(
                and_(
                    UserFollow.follower_id == follower_id,
                    UserFollow.following_id == following_id
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_followers(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 50) -> List[UserFollow]:
        """Get list of followers for a user."""
        result = await db.execute(
            select(UserFollow)
            .options(selectinload(UserFollow.follower))
            .where(UserFollow.following_id == user_id)
            .order_by(UserFollow.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_following(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 50) -> List[UserFollow]:
        """Get list of users that a user is following."""
        result = await db.execute(
            select(UserFollow)
            .options(selectinload(UserFollow.following))
            .where(UserFollow.follower_id == user_id)
            .order_by(UserFollow.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_followers_count(self, db: AsyncSession, user_id: int) -> int:
        """Get count of followers for a user."""
        result = await db.execute(
            select(func.count(UserFollow.id)).where(UserFollow.following_id == user_id)
        )
        return result.scalar() or 0

    async def get_following_count(self, db: AsyncSession, user_id: int) -> int:
        """Get count of users that a user is following."""
        result = await db.execute(
            select(func.count(UserFollow.id)).where(UserFollow.follower_id == user_id)
        )
        return result.scalar() or 0

    async def get_follower_ids(self, db: AsyncSession, user_id: int) -> List[int]:
        """Get list of follower IDs for a user."""
        result = await db.execute(
            select(UserFollow.follower_id).where(UserFollow.following_id == user_id)
        )
        return [row[0] for row in result.all()]


follow_service = FollowService()
