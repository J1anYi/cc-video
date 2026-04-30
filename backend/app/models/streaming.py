"""Adaptive streaming models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class QualityLevel(enum.Enum):
    AUTO = "auto"
    LOW = "low"      # 480p
    MEDIUM = "medium"  # 720p
    HIGH = "high"    # 1080p
    ULTRA = "ultra"  # 4K


class AdaptiveStreamVariant(Base):
    """Stream variant for adaptive bitrate."""
    __tablename__ = "adaptive_stream_variants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    quality: Mapped[QualityLevel] = mapped_column(SQLEnum(QualityLevel), nullable=False)
    resolution: Mapped[str] = mapped_column(String(20), nullable=False)  # 1920x1080
    bitrate: Mapped[int] = mapped_column(Integer, nullable=False)  # kbps
    
    hls_url: Mapped[str] = mapped_column(String(500), nullable=False)
    manifest_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    file_size: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class BandwidthMetric(Base):
    """Bandwidth measurement for analytics."""
    __tablename__ = "bandwidth_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    movie_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("movies.id"), nullable=True)

    bandwidth_kbps: Mapped[int] = mapped_column(Integer, nullable=False)
    quality_selected: Mapped[QualityLevel] = mapped_column(SQLEnum(QualityLevel), nullable=True)
    quality_played: Mapped[QualityLevel] = mapped_column(SQLEnum(QualityLevel), nullable=True)
    
    buffer_events: Mapped[int] = mapped_column(Integer, default=0)
    rebuffer_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class QualityPreference(Base):
    """User quality preference."""
    __tablename__ = "quality_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False)

    preferred_quality: Mapped[QualityLevel] = mapped_column(
        SQLEnum(QualityLevel), 
        default=QualityLevel.AUTO
    )
    auto_adjust: Mapped[bool] = mapped_column(default=True)
    limit_mobile_data: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
