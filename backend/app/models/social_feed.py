"""Social Feed models for personalized activity streams."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class FeedItemType(enum.Enum):
    REVIEW = "review"
    WATCHLIST_ADD = "watchlist_add"
    FAVORITE = "favorite"
    FOLLOW = "follow"
    DISCUSSION = "discussion"
    WATCH_PARTY = "watch_party"
    ACHIEVEMENT = "achievement"


class SocialFeed(Base):
    """User social feed entry."""
    __tablename__ = "social_feeds"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    actor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    item_type: Mapped[FeedItemType] = mapped_column(SQLEnum(FeedItemType), nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    movie_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("movies.id"), nullable=True)
    
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class FeedPreference(Base):
    """User feed preferences."""
    __tablename__ = "feed_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    show_reviews: Mapped[bool] = mapped_column(Boolean, default=True)
    show_watchlist: Mapped[bool] = mapped_column(Boolean, default=True)
    show_favorites: Mapped[bool] = mapped_column(Boolean, default=True)
    show_discussions: Mapped[bool] = mapped_column(Boolean, default=True)
    show_achievements: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class TrendingDiscussion(Base):
    """Trending discussion tracking."""
    __tablename__ = "trending_discussions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    discussion_type: Mapped[str] = mapped_column(String(50), nullable=False)
    discussion_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    score: Mapped[float] = mapped_column(default=0.0)
    reply_count: Mapped[int] = mapped_column(Integer, default=0)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    
    calculated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class FollowRecommendation(Base):
    """Follow recommendation for users."""
    __tablename__ = "follow_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    recommended_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    reason: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
