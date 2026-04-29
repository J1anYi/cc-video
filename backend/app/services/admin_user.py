from datetime import datetime
from typing import Optional
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class AdminUserService:
    async def list_users(
        self,
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
    ) -> tuple[list[User], int]:
        """List users with pagination and optional search."""
        query = select(User).where(User.deleted_at.is_(None))

        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    User.email.ilike(search_term),
                    User.display_name.ilike(search_term),
                )
            )

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar()

        # Apply pagination
        query = query.order_by(User.created_at.desc())
        query = query.offset((page - 1) * limit).limit(limit)

        result = await db.execute(query)
        users = list(result.scalars().all())

        return users, total

    async def get_user_details(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user details by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def suspend_user(
        self, db: AsyncSession, user_id: int, suspend: bool = True
    ) -> Optional[User]:
        """Suspend or unsuspend a user."""
        user = await self.get_user_details(db, user_id)
        if not user:
            return None

        user.is_suspended = suspend
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
        return user

    async def delete_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """Soft delete a user."""
        user = await self.get_user_details(db, user_id)
        if not user:
            return None

        user.deleted_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
        return user


admin_user_service = AdminUserService()
