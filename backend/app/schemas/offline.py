"""Offline and sync schemas for CC Video API."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DownloadQuality(str, Enum):
    Q360P = "360p"
    Q480P = "480p"
    Q720P = "720p"
    Q1080P = "1080p"


class DownloadStatus(str, Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class NetworkType(str, Enum):
    WIFI = "wifi"
    CELLULAR = "cellular"
    METERED = "metered"
    OFFLINE = "offline"


class DownloadRequest(BaseModel):
    movie_id: int
    quality: DownloadQuality = DownloadQuality.Q720P
    wifi_only: bool = True


class DownloadResponse(BaseModel):
    id: int
    movie_id: int
    movie_title: str
    quality: str
    status: str
    progress: float
    file_size: int
    downloaded_bytes: int
    download_speed: Optional[int] = None
    eta_seconds: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class DownloadQueueResponse(BaseModel):
    queue: List[DownloadResponse]
    active_downloads: int
    queued_downloads: int
    total_storage_bytes: int
    available_storage_bytes: int


class SyncProgress(BaseModel):
    last_sync_at: datetime
    pending_items: int
    sync_status: str
    conflicts: int


class WatchProgressSync(BaseModel):
    movie_id: int
    position_seconds: int
    duration_seconds: int
    completed: bool
    updated_at: datetime


class PreferenceSync(BaseModel):
    preference_key: str
    preference_value: str
    updated_at: datetime


class PreloadSuggestion(BaseModel):
    movie_id: int
    movie_title: str
    reason: str
    confidence: float
    estimated_size: int


class OfflineLicense(BaseModel):
    movie_id: int
    license_key: str
    expires_at: datetime
    renewal_url: str


class NetworkStatus(BaseModel):
    network_type: NetworkType
    is_metered: bool
    is_wifi: bool
    signal_strength: Optional[int] = None
    download_speed: Optional[int] = None
