from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.activity import ActivityResponse, ActivityListResponse
from app.services.activity import activity_service


router = APIRouter(prefix="/api", tags=["feed"])


@router.get("/feed", response_model=ActivityListResponse)
async def get_feed(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
):
    """Get activity feed from followed users."""
    activities, total = await activity_service.get_feed(db, current_user.id, skip, limit)
    return ActivityListResponse(
        activities=[
            ActivityResponse(
                id=a.id,
                user_id=a.user_id,
                username=a.user.display_name if a.user else None,
                activity_type=a.activity_type,
                movie_id=a.movie_id,
                movie_title=a.movie.title if a.movie else None,
                reference_id=a.reference_id,
                created_at=a.created_at,
            )
            for a in activities
        ],
        total=total,
    )
