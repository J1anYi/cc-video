"""Creator platform models."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class ContentType(str, enum.Enum):
    VIDEO = "video"
    LIVE = "live"
    SHORT = "short"


class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class CreatorProfile(Base):
    """Creator profile with analytics and settings."""
    __tablename__ = "creator_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    channel_name = Column(String(100), nullable=False)
    channel_description = Column(String(500), nullable=True)
    channel_art_url = Column(String(500), nullable=True)
    subscriber_count = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_watch_time = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    is_partner = Column(Boolean, default=False)
    monetization_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="creator_profile")
    contents = relationship("CreatorContent", back_populates="creator")
    team_members = relationship("CreatorTeamMember", back_populates="creator")


class CreatorContent(Base):
    """Content managed by creators."""
    __tablename__ = "creator_contents"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=True)
    content_type = Column(String(20), default="video")
    status = Column(String(20), default="draft")
    thumbnail_url = Column(String(500), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    tags = Column(JSON, default=list)
    content_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("CreatorProfile", back_populates="contents")
    analytics = relationship("CreatorContentAnalytics", back_populates="content", uselist=False)


class CreatorContentAnalytics(Base):
    """Analytics for creator content."""
    __tablename__ = "creator_content_analytics"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), unique=True, nullable=False)
    views = Column(Integer, default=0)
    unique_viewers = Column(Integer, default=0)
    average_watch_time = Column(Float, default=0.0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    estimated_revenue = Column(Float, default=0.0)
    demographics = Column(JSON, default=dict)
    traffic_sources = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    content = relationship("CreatorContent", back_populates="analytics")


class CreatorTeamMember(Base):
    """Team member with role-based permissions."""
    __tablename__ = "creator_team_members"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="viewer")
    permissions = Column(JSON, default=list)
    invited_at = Column(DateTime, default=datetime.utcnow)
    joined_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    creator = relationship("CreatorProfile", back_populates="team_members")
    user = relationship("User")
