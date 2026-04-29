from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.social_analytics import social_analytics_service

router = APIRouter(prefix="/api/users/me/social-analytics", tags=["social-analytics"])


@router.get("")
async def get_social_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's social analytics."""
    return await social_analytics_service.get_social_analytics(db, current_user.id)


@router.get("/refresh")
async def refresh_social_analytics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Refresh social metrics."""
    return await social_analytics_service.refresh_metrics(db, current_user.id)


@router.get("/compare/{user_id}")
async def compare_with_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compare social stats with another user."""
    return await social_analytics_service.compare_with_user(db, current_user.id, user_id)
