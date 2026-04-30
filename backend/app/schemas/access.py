"""Access control schemas."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.access import AccessLevel, TimeWindowType, PermissionType


class AccessPolicyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    default_level: AccessLevel = AccessLevel.FULL
    max_devices: int = 5
    max_concurrent_streams: int = 2


class AccessPolicyResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    description: Optional[str]
    default_level: AccessLevel
    max_devices: int
    max_concurrent_streams: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ContentPermissionCreate(BaseModel):
    content_id: int
    content_type: str = "movie"
    user_id: Optional[int] = None
    role_id: Optional[int] = None
    permission_type: PermissionType = PermissionType.VIEW
    access_level: AccessLevel = AccessLevel.FULL
    expires_at: Optional[datetime] = None


class ContentPermissionResponse(BaseModel):
    id: int
    content_id: int
    content_type: str
    user_id: Optional[int]
    permission_type: PermissionType
    access_level: AccessLevel
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True


class AccessCheckRequest(BaseModel):
    content_id: int
    content_type: str = "movie"
    device_id: str
    permission_type: PermissionType = PermissionType.VIEW


class AccessCheckResponse(BaseModel):
    allowed: bool
    access_level: AccessLevel
    reason: Optional[str]
    session_token: Optional[str]


class StreamSessionResponse(BaseModel):
    id: int
    content_id: int
    content_type: str
    device_id: str
    started_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class TimeWindowCreate(BaseModel):
    policy_id: int
    window_type: TimeWindowType
    start_hour: int = 0
    end_hour: int = 24
    days_of_week: str = "0,1,2,3,4,5,6"
    timezone: str = "UTC"
