"""Video watermark models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class WatermarkType(enum.Enum):
    VISIBLE = "visible"
    FORENSIC = "forensic"
    USER_SPECIFIC = "user_specific"


class WatermarkPosition(enum.Enum):
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    CENTER = "center"
    CUSTOM = "custom"


class WatermarkStatus(enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    EXPIRED = "expired"


class WatermarkConfiguration(Base):
    """Watermark configuration per tenant."""
    __tablename__ = "watermark_configurations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    default_type: Mapped[WatermarkType] = mapped_column(SQLEnum(WatermarkType), default=WatermarkType.VISIBLE)
    default_position: Mapped[WatermarkPosition] = mapped_column(SQLEnum(WatermarkPosition), default=WatermarkPosition.BOTTOM_RIGHT)
    
    default_opacity: Mapped[float] = mapped_column(Float, default=0.3)
    default_scale: Mapped[float] = mapped_column(Float, default=0.15)
    
    custom_x: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    custom_y: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    forensic_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    forensic_strength: Mapped[int] = mapped_column(Integer, default=50)
    
    user_watermark_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Watermark(Base):
    """Watermark definition."""
    __tablename__ = "watermarks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[WatermarkType] = mapped_column(SQLEnum(WatermarkType), nullable=False)
    
    image_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    text_content: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    position: Mapped[WatermarkPosition] = mapped_column(SQLEnum(WatermarkPosition), default=WatermarkPosition.BOTTOM_RIGHT)
    
    opacity: Mapped[float] = mapped_column(Float, default=0.3)
    scale: Mapped[float] = mapped_column(Float, default=0.15)
    
    custom_x: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    custom_y: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    font_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    font_color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    status: Mapped[WatermarkStatus] = mapped_column(SQLEnum(WatermarkStatus), default=WatermarkStatus.ACTIVE)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class WatermarkSession(Base):
    """Per-session watermark tracking."""
    __tablename__ = "watermark_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    watermark_id: Mapped[int] = mapped_column(Integer, ForeignKey("watermarks.id"), nullable=True)
    
    watermark_data: Mapped[str] = mapped_column(Text, nullable=False)
    
    position: Mapped[WatermarkPosition] = mapped_column(SQLEnum(WatermarkPosition))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ForensicWatermark(Base):
    """Forensic watermark record."""
    __tablename__ = "forensic_watermarks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    pattern_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    embedded_data: Mapped[str] = mapped_column(String(500), nullable=False)
    
    strength: Mapped[int] = mapped_column(Integer, default=50)
    
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    device_info: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LeakTrace(Base):
    """Leak investigation record."""
    __tablename__ = "leak_traces"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    forensic_watermark_id: Mapped[int] = mapped_column(Integer, ForeignKey("forensic_watermarks.id"), nullable=False)
    
    source_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    source_session_id: Mapped[str] = mapped_column(String(100), nullable=False)
    
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    detected_source: Mapped[str] = mapped_column(String(200), nullable=True)
    
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    status: Mapped[str] = mapped_column(String(50), default="investigating")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
