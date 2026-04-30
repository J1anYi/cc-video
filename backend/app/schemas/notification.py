from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    NEW_CONTENT = "new_content"
    DOWNLOAD_COMPLETE = "download_complete"
    WATCH_PARTY = "watch_party"
    RECOMMENDATION = "recommendation"
    SOCIAL = "social"
    SYSTEM = "system"

class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

class PushNotification(BaseModel):
    title: str
    body: str
    icon: Optional[str] = None
    image: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, str]]] = None

class NotificationRequest(BaseModel):
    user_id: int
    notification_type: NotificationType
    priority: NotificationPriority = NotificationPriority.NORMAL
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None

class NotificationResponse(BaseModel):
    id: int
    notification_type: NotificationType
    title: str
    body: str
    read: bool
    created_at: datetime


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    unread: int


class UnreadCountResponse(BaseModel):
    unread_count: int


class NotificationPreferences(BaseModel):
    new_content: bool = True
    download_complete: bool = True
    watch_party: bool = True
    recommendations: bool = True
    social: bool = True
    quiet_hours_start: Optional[str] = "22:00"
    quiet_hours_end: Optional[str] = "08:00"
