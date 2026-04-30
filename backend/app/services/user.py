from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.services.auth import auth_service


class UserService:
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, email: str, password: str, role: UserRole = UserRole.USER) -> User:
        hashed_password = auth_service.get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user_service = UserService()
