from typing import List, Tuple, Optional
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.user_block import UserBlock
from app.models.user import User


class UserBlockService:
    """Service for managing user block relationships."""

    async def block_user(
        self, db: AsyncSession, blocker_id: int, blocked_id: int
    ) -> UserBlock:
        """Block a user."""
        if blocker_id == blocked_id:
            raise ValueError("Cannot block yourself")
        
        block = UserBlock(blocker_id=blocker_id, blocked_id=blocked_id)
        db.add(block)
        await db.commit()
        await db.refresh(block)
        return block

    async def unblock_user(
        self, db: AsyncSession, blocker_id: int, blocked_id: int
    ) -> bool:
        """Unblock a user. Returns True if unblocked, False if not found."""
        result = await db.execute(
            select(UserBlock).where(
                UserBlock.blocker_id == blocker_id,
                UserBlock.blocked_id == blocked_id
            )
        )
        block = result.scalar_one_or_none()
        if not block:
            return False
        
        await db.delete(block)
        await db.commit()
        return True

    async def is_blocked(
        self, db: AsyncSession, user_id: int, other_user_id: int
    ) -> bool:
        """Check if user_id has blocked other_user_id."""
        result = await db.execute(
            select(UserBlock).where(
                UserBlock.blocker_id == user_id,
                UserBlock.blocked_id == other_user_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def is_blocked_either_direction(
        self, db: AsyncSession, user1_id: int, user2_id: int
    ) -> bool:
        """Check if either user has blocked the other."""
        result = await db.execute(
            select(UserBlock).where(
                or_(
                    and_(UserBlock.blocker_id == user1_id, UserBlock.blocked_id == user2_id),
                    and_(UserBlock.blocker_id == user2_id, UserBlock.blocked_id == user1_id)
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_blocked_users(
        self, db: AsyncSession, blocker_id: int
    ) -> List[Tuple[UserBlock, User]]:
        """Get list of users blocked by blocker_id."""
        result = await db.execute(
            select(UserBlock, User)
            .join(User, UserBlock.blocked_id == User.id)
            .where(UserBlock.blocker_id == blocker_id)
            .order_by(UserBlock.created_at.desc())
        )
        return list(result.all())

    async def get_blocked_user_ids(
        self, db: AsyncSession, blocker_id: int
    ) -> List[int]:
        """Get list of user IDs blocked by blocker_id."""
        result = await db.execute(
            select(UserBlock.blocked_id).where(UserBlock.blocker_id == blocker_id)
        )
        return [row[0] for row in result.all()]


user_block_service = UserBlockService()
