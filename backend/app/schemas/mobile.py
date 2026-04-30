"""Mobile platform schemas for CC Video API."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PlatformEnum(str, Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class DeviceInfo(BaseModel):
    platform: PlatformEnum
    device_id: str
    device_name: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None


class PushTokenCreate(BaseModel):
    device_id: str
    platform: PlatformEnum
    push_token: str


class PushTokenResponse(BaseModel):
    id: int
    device_id: str
    platform: PlatformEnum
    push_token: str
    created_at: datetime


class MobileAppConfig(BaseModel):
    min_app_version: str
    latest_app_version: str
    force_update: bool
    maintenance_mode: bool
    feature_flags: dict


class PWAManifestIcon(BaseModel):
    src: str
    sizes: str
    type: str
    purpose: Optional[str] = None


class PWAManifest(BaseModel):
    name: str
    short_name: str
    description: str
    start_url: str
    display: str
    background_color: str
    theme_color: str
    icons: List[PWAManifestIcon]


class MobileDownloadRequest(BaseModel):
    movie_id: int
    quality: str = "720p"
    wifi_only: bool = True


class MobileDownloadStatus(BaseModel):
    id: int
    movie_id: int
    movie_title: str
    quality: str
    status: str
    progress: float
    file_size: int
    downloaded_bytes: int
    created_at: datetime
    completed_at: Optional[datetime] = None


class OfflineContentResponse(BaseModel):
    downloads: List[MobileDownloadStatus]
    total_storage_bytes: int
    max_storage_bytes: int
