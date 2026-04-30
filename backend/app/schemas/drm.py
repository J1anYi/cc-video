"""DRM schemas for API validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.drm import DRMProvider, DRMKeyStatus, DeviceType


class DRMConfigCreate(BaseModel):
    provider: DRMProvider
    widevine_license_url: Optional[str] = None
    widevine_provider_id: Optional[str] = None
    playready_license_url: Optional[str] = None
    playready_key_id: Optional[str] = None
    fairplay_license_url: Optional[str] = None
    fairplay_cert_url: Optional[str] = None
    max_devices_per_user: int = 5
    offline_playback_enabled: bool = False
    offline_duration_hours: int = 168
    key_rotation_days: int = 30


class DRMConfigResponse(BaseModel):
    id: int
    tenant_id: int
    provider: DRMProvider
    widevine_license_url: Optional[str]
    playready_license_url: Optional[str]
    fairplay_license_url: Optional[str]
    max_devices_per_user: int
    offline_playback_enabled: bool
    offline_duration_hours: int
    key_rotation_days: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DRMKeyCreate(BaseModel):
    content_id: int
    content_type: str = "movie"
    provider: DRMProvider


class DRMKeyResponse(BaseModel):
    id: int
    key_id: str
    content_id: int
    content_type: str
    provider: DRMProvider
    status: DRMKeyStatus
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True


class LicenseRequest(BaseModel):
    content_id: int
    content_type: str = "movie"
    device_id: str
    provider: DRMProvider


class LicenseResponse(BaseModel):
    license_token: str
    key_id: str
    provider: DRMProvider
    content_id: int
    issued_at: datetime
    expires_at: datetime


class DeviceRegisterRequest(BaseModel):
    device_id: str
    device_name: Optional[str] = None
    device_type: DeviceType = DeviceType.UNKNOWN
    drm_provider: DRMProvider


class DeviceResponse(BaseModel):
    id: int
    device_id: str
    device_name: Optional[str]
    device_type: DeviceType
    drm_provider: DRMProvider
    is_active: bool
    last_used_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class OfflineTokenRequest(BaseModel):
    content_id: int
    content_type: str = "movie"
    device_id: str
    provider: DRMProvider


class OfflineTokenResponse(BaseModel):
    token: str
    content_id: int
    device_id: int
    expires_at: datetime
    encrypted_key: str


class KeyRotationRequest(BaseModel):
    content_id: int
    content_type: str = "movie"


class KeyRotationResponse(BaseModel):
    old_key_id: str
    new_key_id: str
    rotated_at: datetime
