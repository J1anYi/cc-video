"""Mobile platform database models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class PlatformEnum(enum.Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


class DownloadStatus(enum.Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class PushToken(Base):
    __tablename__ = "push_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(String(255), nullable=False)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    push_token = Column(String(512), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="push_tokens")


class MobileDownload(Base):
    __tablename__ = "mobile_downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    device_id = Column(String(255), nullable=False)
    quality = Column(String(20), default="720p")
    status = Column(SQLEnum(DownloadStatus), default=DownloadStatus.PENDING)
    progress = Column(Float, default=0.0)
    file_size = Column(Integer, default=0)
    downloaded_bytes = Column(Integer, default=0)
    storage_path = Column(String(512), nullable=True)
    license_key = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="downloads")
    movie = relationship("Movie", backref="downloads")


class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(String(255), nullable=False)
    device_name = Column(String(255), nullable=True)
    platform = Column(SQLEnum(PlatformEnum), nullable=False)
    os_version = Column(String(50), nullable=True)
    app_version = Column(String(20), nullable=True)
    last_active = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="devices")
