"""Forum models for community discussions."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class ThreadStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PINNED = "pinned"
    HIDDEN = "hidden"


class Forum(Base):
    """Discussion forum category."""
    __tablename__ = "forums"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    category: Mapped[str] = mapped_column(String(50), default="general")
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    thread_count: Mapped[int] = mapped_column(Integer, default=0)
    post_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class ForumThread(Base):
    """Forum discussion thread."""
    __tablename__ = "forum_threads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    forum_id: Mapped[int] = mapped_column(Integer, ForeignKey("forums.id"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    status: Mapped[ThreadStatus] = mapped_column(SQLEnum(ThreadStatus), default=ThreadStatus.OPEN)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    reply_count: Mapped[int] = mapped_column(Integer, default=0)
    
    last_post_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_post_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class ForumPost(Base):
    """Post in a forum thread."""
    __tablename__ = "forum_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    thread_id: Mapped[int] = mapped_column(Integer, ForeignKey("forum_threads.id"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)


class ForumModeration(Base):
    """Moderation action log."""
    __tablename__ = "forum_moderations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    moderator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False)
    
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
