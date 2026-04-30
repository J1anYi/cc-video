from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.notification import (
    PushNotification, NotificationRequest, NotificationResponse,
    NotificationPreferences, NotificationType
)
from datetime import datetime

router = APIRouter(prefix="/mobile/notifications", tags=["mobile-notifications"])

def get_current_user_id(x_user_id: str = Header(...)) -> int:
    return int(x_user_id)

@router.post("/send")
def send_notification(
    request: NotificationRequest,
    db: Session = Depends(get_db)
):
    return {"status": "sent", "notification_id": 1}

@router.get("", response_model=List[NotificationResponse])
def get_notifications(
    user_id: int = Depends(get_current_user_id),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return []

@router.get("/preferences", response_model=NotificationPreferences)
def get_preferences(user_id: int = Depends(get_current_user_id)):
    return NotificationPreferences()

@router.put("/preferences", response_model=NotificationPreferences)
def update_preferences(
    preferences: NotificationPreferences,
    user_id: int = Depends(get_current_user_id)
):
    return preferences

@router.post("/{notification_id}/read")
def mark_read(notification_id: int):
    return {"status": "read"}

@router.post("/read-all")
def mark_all_read(user_id: int = Depends(get_current_user_id)):
    return {"status": "all_read"}
