from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.user import User
from app.models.tenant import Tenant
from app.services.auth import auth_service
from app.services.user import user_service
from app.services.tenant_service import tenant_service


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


security = HTTPBearer()


async def get_current_tenant(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[Tenant]:
    tenant = getattr(request.state, 'tenant', None)
    if tenant:
        return tenant
    tenant_id = getattr(request.state, 'tenant_id', None)
    if tenant_id:
        return await tenant_service.get_by_id(db, tenant_id)
    return None


async def get_current_tenant_id(
    request: Request,
) -> Optional[int]:
    return getattr(request.state, 'tenant_id', None)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
    request: Request = None,
) -> User:
    token = credentials.credentials
    payload = auth_service.decode_token(token)

    if payload is None or payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_by_id(db, int(payload.sub))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive",
        )

    if request and not getattr(request.state, 'tenant_id', None):
        if user.tenant_id:
            request.state.tenant_id = user.tenant_id

    return user


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    if payload is None or payload.type != "access":
        return None
    user = await user_service.get_by_id(db, int(payload.sub))
    if user is None or not user.is_active:
        return None
    return user


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


async def require_platform_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_platform_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform admin access required",
        )
    return current_user


async def require_tenant(
    tenant: Optional[Tenant] = Depends(get_current_tenant),
) -> Tenant:
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required",
        )
    return tenant
