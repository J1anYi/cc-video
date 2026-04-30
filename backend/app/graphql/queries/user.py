import strawberry
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from strawberry.types import Info

from app.models.user import User
from app.graphql.types import UserType, UserProfile


@strawberry.type
class UserQuery:
    @strawberry.field
    async def me(self, info: Info) -> Optional[UserType]:
        user = info.context.get("user")
        if not user:
            return None
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @strawberry.field
    async def user(self, info: Info, user_id: int) -> Optional[UserType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @strawberry.field
    async def users(self, info: Info, limit: int = 10, offset: int = 0) -> List[UserType]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(User).limit(limit).offset(offset))
        users = result.scalars().all()
        return [
            UserType(
                id=u.id,
                username=u.username,
                email=u.email,
                is_admin=u.is_admin,
                is_active=u.is_active,
                created_at=u.created_at,
                updated_at=u.updated_at,
            )
            for u in users
        ]
