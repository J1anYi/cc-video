from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime


class PredictionModel(Base):
    """Metadata for prediction models."""
    __tablename__ = "prediction_models"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.0")
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_trained: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ContentPrediction(Base):
    """Content success predictions."""
    __tablename__ = "content_predictions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    success_score: Mapped[float] = mapped_column(Float, default=0.0)
    predicted_views: Mapped[int] = mapped_column(Integer, default=0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    factors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    predicted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    content = relationship("Movie", backref="predictions")


class DemandForecast(Base):
    """Demand forecasts for content."""
    __tablename__ = "demand_forecasts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=True, index=True)
    genre: Mapped[str | None] = mapped_column(String(50), nullable=True)
    forecast_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    predicted_views: Mapped[int] = mapped_column(Integer, default=0)
    predicted_hours: Mapped[int] = mapped_column(Integer, default=0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PricingSuggestion(Base):
    """Pricing recommendations."""
    __tablename__ = "pricing_suggestions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    plan: Mapped[str] = mapped_column(String(50), nullable=False)
    current_price: Mapped[float] = mapped_column(Float, default=0.0)
    suggested_price: Mapped[float] = mapped_column(Float, default=0.0)
    expected_revenue_change: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    reasoning: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ContentGap(Base):
    """Content gap analysis results."""
    __tablename__ = "content_gaps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    demand_score: Mapped[float] = mapped_column(Float, default=0.0)
    supply_score: Mapped[float] = mapped_column(Float, default=0.0)
    gap_score: Mapped[float] = mapped_column(Float, default=0.0)
    recommendation: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
