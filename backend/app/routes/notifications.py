from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationListResponse, UnreadCountResponse
from app.services.notification import notification_service


router = APIRouter(prefix="/api", tags=["notifications"])


@router.get("/notifications", response_model=NotificationListResponse)
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = False,
):
    notifications, total, unread_count = await notification_service.get_notifications(
        db, current_user.id, skip, limit, unread_only
    )
    return NotificationListResponse(
        notifications=[
            NotificationResponse(
                id=n.id,
                notification_type=n.notification_type,
                title=n.title,
                content=n.content,
                actor_id=n.actor_id,
                actor_name=n.actor.display_name if n.actor else None,
                target_type=n.target_type,
                target_id=n.target_id,
                is_read=n.is_read,
                created_at=n.created_at,
            )
            for n in notifications
        ],
        total=total,
        unread_count=unread_count,
    )


@router.patch("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = await notification_service.mark_as_read(db, current_user.id, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}


@router.patch("/notifications/read-all")
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = await notification_service.mark_all_as_read(db, current_user.id)
    return {"message": f"Marked {count} notifications as read"}


@router.get("/notifications/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = await notification_service.get_unread_count(db, current_user.id)
    return UnreadCountResponse(unread_count=count)
