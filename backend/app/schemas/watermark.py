"""Watermark schemas for API validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.watermark import WatermarkType, WatermarkPosition, WatermarkStatus


class WatermarkConfigCreate(BaseModel):
    default_type: WatermarkType = WatermarkType.VISIBLE
    default_position: WatermarkPosition = WatermarkPosition.BOTTOM_RIGHT
    default_opacity: float = 0.3
    default_scale: float = 0.15
    custom_x: Optional[int] = None
    custom_y: Optional[int] = None
    forensic_enabled: bool = False
    forensic_strength: int = 50
    user_watermark_enabled: bool = True


class WatermarkConfigResponse(BaseModel):
    id: int
    tenant_id: int
    default_type: WatermarkType
    default_position: WatermarkPosition
    default_opacity: float
    default_scale: float
    forensic_enabled: bool
    user_watermark_enabled: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class WatermarkCreate(BaseModel):
    name: str
    type: WatermarkType
    image_path: Optional[str] = None
    text_content: Optional[str] = None
    position: WatermarkPosition = WatermarkPosition.BOTTOM_RIGHT
    opacity: float = 0.3
    scale: float = 0.15
    custom_x: Optional[int] = None
    custom_y: Optional[int] = None
    font_size: Optional[int] = None
    font_color: Optional[str] = None


class WatermarkResponse(BaseModel):
    id: int
    name: str
    type: WatermarkType
    image_path: Optional[str]
    text_content: Optional[str]
    position: WatermarkPosition
    opacity: float
    scale: float
    status: WatermarkStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ApplyWatermarkRequest(BaseModel):
    content_id: int
    content_type: str = "movie"
    watermark_id: Optional[int] = None
    session_id: str
    user_specific_text: Optional[str] = None


class ForensicRequest(BaseModel):
    content_id: int
    content_type: str = "movie"
    session_id: str
    strength: int = 50


class ForensicResponse(BaseModel):
    pattern_id: str
    embedded_data: str
    content_id: int
    created_at: datetime


class TraceRequest(BaseModel):
    sample_data: str
    content_id: Optional[int] = None


class TraceResponse(BaseModel):
    found: bool
    source_user_id: Optional[int]
    source_session_id: Optional[str]
    confidence_score: float
    trace_id: int
