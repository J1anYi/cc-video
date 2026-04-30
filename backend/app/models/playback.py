"""Playback settings models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class PlaybackSpeed(enum.Enum):
    SLOW = "0.5x"
    NORMAL = "1x"
    FAST = "1.5x"
    FASTER = "2x"


class PlaybackSettings(Base):
    """User playback settings."""
    __tablename__ = "playback_settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False)

    default_speed: Mapped[float] = mapped_column(Float, default=1.0)
    auto_skip_intro: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_skip_credits: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_next_episode: Mapped[bool] = mapped_column(Boolean, default=True)
    pip_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    keyboard_shortcuts: Mapped[Optional[dict]] = mapped_column(default=None)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class WatchProgress(Base):
    """Watch progress for sync across devices."""
    __tablename__ = "watch_progress"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False)

    position_seconds: Mapped[int] = mapped_column(Integer, default=0)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    completion_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    
    last_played_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
