"""Access control models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class AccessLevel(enum.Enum):
    FULL = "full"
    LIMITED = "limited"
    PREVIEW = "preview"
    NONE = "none"


class TimeWindowType(enum.Enum):
    ALLOWED = "allowed"
    RESTRICTED = "restricted"


class PermissionType(enum.Enum):
    VIEW = "view"
    DOWNLOAD = "download"
    SHARE = "share"


class AccessPolicy(Base):
    """Access policy definition."""
    __tablename__ = "access_policies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    default_level: Mapped[AccessLevel] = mapped_column(SQLEnum(AccessLevel), default=AccessLevel.FULL)
    
    max_devices: Mapped[int] = mapped_column(Integer, default=5)
    max_concurrent_streams: Mapped[int] = mapped_column(Integer, default=2)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContentPermission(Base):
    """Content-level permissions."""
    __tablename__ = "content_permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    role_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    permission_type: Mapped[PermissionType] = mapped_column(SQLEnum(PermissionType), default=PermissionType.VIEW)
    access_level: Mapped[AccessLevel] = mapped_column(SQLEnum(AccessLevel), default=AccessLevel.FULL)
    
    granted_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class TimeWindow(Base):
    """Time-based access windows."""
    __tablename__ = "time_windows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    policy_id: Mapped[int] = mapped_column(Integer, ForeignKey("access_policies.id"), nullable=False)
    
    window_type: Mapped[TimeWindowType] = mapped_column(SQLEnum(TimeWindowType), nullable=False)
    
    start_hour: Mapped[int] = mapped_column(Integer, default=0)
    end_hour: Mapped[int] = mapped_column(Integer, default=24)
    
    days_of_week: Mapped[str] = mapped_column(String(20), default="0,1,2,3,4,5,6")
    
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DeviceLimit(Base):
    """Device limit configuration."""
    __tablename__ = "device_limits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    max_devices: Mapped[int] = mapped_column(Integer, default=5)
    current_devices: Mapped[int] = mapped_column(Integer, default=0)
    
    max_streams: Mapped[int] = mapped_column(Integer, default=2)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StreamSession(Base):
    """Active stream sessions."""
    __tablename__ = "stream_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    device_id: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    session_token: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
