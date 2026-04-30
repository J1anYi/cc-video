import strawberry
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from strawberry.types import Info

from app.models.user import User
from app.graphql.types import UserType, UserUpdateInput


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def update_profile(self, info: Info, input: UserUpdateInput) -> Optional[UserType]:
        user = info.context.get("user")
        if not user:
            return None
        
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(User).where(User.id == user.id))
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        if input.username:
            db_user.username = input.username
        if input.email:
            db_user.email = input.email
        
        await db.commit()
        await db.refresh(db_user)
        
        return UserType(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_admin=db_user.is_admin,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )
