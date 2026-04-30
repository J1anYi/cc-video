"""Live streaming models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Text
from app.database import Base
import uuid


class CreatorLiveStream(Base):
    """Live stream session for creators."""
    __tablename__ = "creator_live_streams"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    stream_key = Column(String(100), unique=True, default=lambda: str(uuid.uuid4()))
    playback_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    status = Column(String(50), default="offline")
    is_recording = Column(Boolean, default=False)
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    viewer_count = Column(Integer, default=0)
    peak_viewers = Column(Integer, default=0)
    duration = Column(Integer, default=0)
    tags = Column(JSON, default=list)
    config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LiveChatMessage(Base):
    """Live chat message."""
    __tablename__ = "live_chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("creator_live_streams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_highlighted = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class LiveStreamRecording(Base):
    """Live stream recording."""
    __tablename__ = "live_stream_recordings"

    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("creator_live_streams.id"), nullable=False)
    video_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    duration = Column(Integer, default=0)
    file_size = Column(Integer, default=0)
    status = Column(String(50), default="processing")
    created_at = Column(DateTime, default=datetime.utcnow)


class CreatorLiveStreamSchedule(Base):
    """Scheduled live stream for creators."""
    __tablename__ = "creator_live_stream_schedules"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=True)
    timezone = Column(String(50), default="UTC")
    reminder_sent = Column(Boolean, default=False)
    stream_id = Column(Integer, ForeignKey("creator_live_streams.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LiveStreamAnalytics(Base):
    """Live stream analytics."""
    __tablename__ = "live_stream_analytics"

    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("creator_live_streams.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    viewer_count = Column(Integer, default=0)
    chat_messages = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    new_followers = Column(Integer, default=0)
    estimated_revenue = Column(Float, default=0.0)
