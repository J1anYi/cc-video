from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime


class Subscription(Base):
    """User subscription tracking."""
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    plan: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")
    monthly_price: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="subscription", uselist=False)


class PaymentTransaction(Base):
    """Payment transaction records."""
    __tablename__ = "payment_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    transaction_type: Mapped[str] = mapped_column(String(50), default="subscription")
    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="transactions")


class RevenueAnalytics(Base):
    """Cached revenue analytics by period."""
    __tablename__ = "revenue_analytics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    period_type: Mapped[str] = mapped_column(String(20), nullable=False)
    period_key: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    new_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    churned_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    net_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    transaction_count: Mapped[int] = mapped_column(Integer, default=0)
    active_subscribers: Mapped[int] = mapped_column(Integer, default=0)
    new_subscribers: Mapped[int] = mapped_column(Integer, default=0)
    churned_subscribers: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RevenuePerUser(Base):
    """Revenue metrics per user."""
    __tablename__ = "revenue_per_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    transaction_count: Mapped[int] = mapped_column(Integer, default=0)
    first_payment_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_payment_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    subscription_months: Mapped[int] = mapped_column(Integer, default=0)
    arpu: Mapped[float] = mapped_column(Float, default=0.0)
    ltv: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="revenue_metrics", uselist=False)
