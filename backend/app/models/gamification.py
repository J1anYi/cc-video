"""Gamification models for achievements and rewards."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, Float
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class BadgeType(enum.Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class AchievementType(enum.Enum):
    WATCH_COUNT = "watch_count"
    REVIEW_COUNT = "review_count"
    SOCIAL = "social"
    ENGAGEMENT = "engagement"
    SPECIAL = "special"


class Badge(Base):
    """Achievement badge definition."""
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon: Mapped[str] = mapped_column(String(255), nullable=False)
    
    badge_type: Mapped[BadgeType] = mapped_column(SQLEnum(BadgeType), default=BadgeType.BRONZE)
    achievement_type: Mapped[AchievementType] = mapped_column(SQLEnum(AchievementType), nullable=False)
    
    xp_reward: Mapped[int] = mapped_column(Integer, default=0)
    requirement: Mapped[int] = mapped_column(Integer, default=1)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class UserBadge(Base):
    """Badge earned by user."""
    __tablename__ = "user_badges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    badge_id: Mapped[int] = mapped_column(Integer, ForeignKey("badges.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    earned_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class UserXP(Base):
    """User XP and level tracking."""
    __tablename__ = "user_xp"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class Leaderboard(Base):
    """Leaderboard entry."""
    __tablename__ = "leaderboards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    score: Mapped[float] = mapped_column(Float, default=0.0)
    rank: Mapped[int] = mapped_column(Integer, default=0)
    
    period: Mapped[str] = mapped_column(String(20), default="all_time")
    calculated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Challenge(Base):
    """Gamification challenge."""
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    xp_reward: Mapped[int] = mapped_column(Integer, default=0)
    requirement_type: Mapped[str] = mapped_column(String(50), nullable=False)
    requirement_count: Mapped[int] = mapped_column(Integer, default=1)
    
    start_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    end_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class UserChallenge(Base):
    """User challenge progress."""
    __tablename__ = "user_challenges"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    challenge_id: Mapped[int] = mapped_column(Integer, ForeignKey("challenges.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    progress: Mapped[int] = mapped_column(Integer, default=0)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    started_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Reward(Base):
    """Unlockable reward."""
    __tablename__ = "rewards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    reward_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    level_required: Mapped[int] = mapped_column(Integer, default=1)
    badge_required: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("badges.id"), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class UserReward(Base):
    """Reward unlocked by user."""
    __tablename__ = "user_rewards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reward_id: Mapped[int] = mapped_column(Integer, ForeignKey("rewards.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    unlocked_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
