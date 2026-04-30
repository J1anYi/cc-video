import strawberry
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from strawberry.types import Info

from app.models.user import User
from app.graphql.types import UserType, UserCreateInput
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    async def login(self, info: Info, username: str, password: str) -> Optional[str]:
        db: AsyncSession = info.context["db"]
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        
        access_token = jwt.encode(
            {
                "sub": str(user.id),
                "exp": datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
            },
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return access_token

    @strawberry.mutation
    async def register(self, info: Info, input: UserCreateInput) -> UserType:
        db: AsyncSession = info.context["db"]
        hashed_password = pwd_context.hash(input.password)
        
        user = User(
            username=input.username,
            email=input.email,
            hashed_password=hashed_password,
            is_admin=False,
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
