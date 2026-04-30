from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime


class UserJourneyEvent(Base):
    """Track user navigation and action events."""
    __tablename__ = "user_journey_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    page_url: Mapped[str] = mapped_column(String(500), nullable=False)
    referrer_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", backref="journey_events")


class UserSessionAnalytics(Base):
    """Aggregated session analytics per user."""
    __tablename__ = "user_session_analytics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    session_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_session_duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    bounce_rate: Mapped[float] = mapped_column(Float, default=0.0)
    peak_hour: Mapped[int] = mapped_column(Integer, default=0)
    last_session_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user = relationship("User", backref="session_analytics", uselist=False)


class UserSegment(Base):
    """User segment definitions."""
    __tablename__ = "user_segments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rules: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CohortAnalytics(Base):
    """Cohort retention analytics."""
    __tablename__ = "cohort_analytics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cohort_key: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    signup_count: Mapped[int] = mapped_column(Integer, default=0)
    d1_retention: Mapped[float | None] = mapped_column(Float, nullable=True)
    d7_retention: Mapped[float | None] = mapped_column(Float, nullable=True)
    d14_retention: Mapped[float | None] = mapped_column(Float, nullable=True)
    d30_retention: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChurnRisk(Base):
    """Churn risk scores for users."""
    __tablename__ = "churn_risks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_factors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_calculated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="churn_risk", uselist=False)
