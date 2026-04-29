from datetime import datetime
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    notification_type: str
    title: str
    content: str | None
    actor_id: int | None
    actor_name: str | None
    target_type: str | None
    target_id: int | None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: list[NotificationResponse]
    total: int
    unread_count: int


class UnreadCountResponse(BaseModel):
    unread_count: int
