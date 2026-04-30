"""Monetization models for creator monetization."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class PayoutStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TipStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class CreatorEarnings(Base):
    """Creator earnings record."""
    __tablename__ = "creator_earnings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # sale, tip, subscription
    source_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    gross_amount: Mapped[float] = mapped_column(Float, nullable=False)
    platform_fee: Mapped[float] = mapped_column(Float, default=0.0)
    net_amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    status: Mapped[str] = mapped_column(String(20), default="available")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Payout(Base):
    """Creator payout record."""
    __tablename__ = "payouts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    status: Mapped[PayoutStatus] = mapped_column(
        SQLEnum(PayoutStatus),
        default=PayoutStatus.PENDING
    )

    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    requested_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    processed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)


class Tip(Base):
    """User tip to creator."""
    __tablename__ = "tips"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    platform_fee: Mapped[float] = mapped_column(Float, default=0.0)
    net_amount: Mapped[float] = mapped_column(Float, nullable=False)

    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[TipStatus] = mapped_column(
        SQLEnum(TipStatus),
        default=TipStatus.PENDING
    )

    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class PremiumContent(Base):
    """Premium gated content."""
    __tablename__ = "premium_content"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    access_type: Mapped[str] = mapped_column(String(20), default="purchase")  # purchase, subscription, tier
    min_tier: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class CreatorTier(Base):
    """Creator subscription tier."""
    __tablename__ = "creator_tiers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    billing_period: Mapped[str] = mapped_column(String(20), default="monthly")

    benefits: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    subscriber_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class CreatorSubscription(Base):
    """User subscription to creator tier."""
    __tablename__ = "creator_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tier_id: Mapped[int] = mapped_column(Integer, ForeignKey("creator_tiers.id"), nullable=False)
    subscriber_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    status: Mapped[SubscriptionStatus] = mapped_column(
        SQLEnum(SubscriptionStatus),
        default=SubscriptionStatus.ACTIVE
    )

    current_period_start: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    current_period_end: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tier: Mapped["CreatorTier"] = relationship("CreatorTier")
