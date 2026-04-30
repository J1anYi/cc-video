from typing import List
from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.user import User


def require_roles(allowed_roles: List[str]):
    """Dependency factory for role-based access control.

    Usage:
        @router.post("/admin/endpoint", dependencies=[Depends(require_roles(["admin"]))])
        async def admin_endpoint():
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return role_checker
