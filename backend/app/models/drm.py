"""Digital Rights Management models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class DRMProvider(enum.Enum):
    WIDEVINE = "widevine"
    PLAYREADY = "playready"
    FAIRPLAY = "fairplay"


class DRMKeyStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class DeviceType(enum.Enum):
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"
    SMART_TV = "smart_tv"
    UNKNOWN = "unknown"


class DRMConfiguration(Base):
    """DRM configuration per tenant."""
    __tablename__ = "drm_configurations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    provider: Mapped[DRMProvider] = mapped_column(SQLEnum(DRMProvider), nullable=False)
    
    widevine_license_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    widevine_provider_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    playready_license_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    playready_key_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    fairplay_license_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    fairplay_cert_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    max_devices_per_user: Mapped[int] = mapped_column(Integer, default=5)
    offline_playback_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    offline_duration_hours: Mapped[int] = mapped_column(Integer, default=168)  # 7 days
    
    key_rotation_days: Mapped[int] = mapped_column(Integer, default=30)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DRMKey(Base):
    """Content encryption key."""
    __tablename__ = "drm_keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    key_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    encryption_key: Mapped[str] = mapped_column(String(500), nullable=False)
    
    provider: Mapped[DRMProvider] = mapped_column(SQLEnum(DRMProvider), nullable=False)
    
    status: Mapped[DRMKeyStatus] = mapped_column(SQLEnum(DRMKeyStatus), default=DRMKeyStatus.ACTIVE)
    
    iv: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rotated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class DeviceRegistration(Base):
    """User device for DRM playback."""
    __tablename__ = "device_registrations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    device_id: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    device_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    device_type: Mapped[DeviceType] = mapped_column(SQLEnum(DeviceType), default=DeviceType.UNKNOWN)
    
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    drm_provider: Mapped[DRMProvider] = mapped_column(SQLEnum(DRMProvider), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class DRMLicense(Base):
    """Issued DRM license."""
    __tablename__ = "drm_licenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    key_id: Mapped[int] = mapped_column(Integer, ForeignKey("drm_keys.id"), nullable=False, index=True)
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey("device_registrations.id"), nullable=True)
    
    license_token: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    provider: Mapped[DRMProvider] = mapped_column(SQLEnum(DRMProvider), nullable=False)
    
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class OfflineDRMToken(Base):
    """Offline playback token."""
    __tablename__ = "offline_drm_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    token: Mapped[str] = mapped_column(String(500), nullable=False, unique=True, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey("device_registrations.id"), nullable=False)
    
    encrypted_key: Mapped[str] = mapped_column(String(500), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    download_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_played_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
