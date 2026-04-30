from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class StreamStatus(enum.Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    ENDED = "ended"
    ERROR = "error"


class LiveStream(Base):
    __tablename__ = "live_streams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    streamer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    status: Mapped[StreamStatus] = mapped_column(SQLEnum(StreamStatus), default=StreamStatus.SCHEDULED)
    
    webrtc_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    hls_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    recording_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    viewer_count: Mapped[int] = mapped_column(Integer, default=0)
    peak_viewers: Mapped[int] = mapped_column(Integer, default=0)
    
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    chats: Mapped[List["LiveChat"]] = relationship("LiveChat", back_populates="stream", cascade="all, delete-orphan")
    reactions: Mapped[List["StreamReaction"]] = relationship("StreamReaction", back_populates="stream", cascade="all, delete-orphan")


class LiveChat(Base):
    __tablename__ = "live_chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stream_id: Mapped[int] = mapped_column(Integer, ForeignKey("live_streams.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_highlighted: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    stream: Mapped["LiveStream"] = relationship("LiveStream", back_populates="chats")


class StreamReaction(Base):
    __tablename__ = "stream_reactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stream_id: Mapped[int] = mapped_column(Integer, ForeignKey("live_streams.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    reaction_type: Mapped[str] = mapped_column(String(20), nullable=False)  # like, heart, fire, etc.
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    stream: Mapped["LiveStream"] = relationship("LiveStream", back_populates="reactions")


class LiveStreamSchedule(Base):
    """Scheduled live stream."""
    __tablename__ = "live_stream_schedules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stream_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("live_streams.id"), nullable=True)
    streamer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    scheduled_start: Mapped[datetime] = mapped_column(nullable=False)
    scheduled_end: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    is_recurring: Mapped[bool] = mapped_column(default=False)
    recurrence_pattern: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    reminder_sent: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class LiveStreamDVR(Base):
    """DVR segment for live stream playback."""
    __tablename__ = "live_stream_dvr"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stream_id: Mapped[int] = mapped_column(Integer, ForeignKey("live_streams.id"), nullable=False, index=True)
    
    segment_url: Mapped[str] = mapped_column(String(500), nullable=False)
    segment_duration: Mapped[int] = mapped_column(Integer, default=10)
    
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class LiveStreamNotification(Base):
    """Notification subscription for live streams."""
    __tablename__ = "live_stream_notifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stream_id: Mapped[int] = mapped_column(Integer, ForeignKey("live_streams.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    notification_type: Mapped[str] = mapped_column(String(20), default="start")
    notify_before_minutes: Mapped[int] = mapped_column(Integer, default=5)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
