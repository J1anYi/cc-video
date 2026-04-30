"""Watermark API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.watermark import WatermarkType, WatermarkPosition
from app.schemas.watermark import (
    WatermarkConfigCreate, WatermarkConfigResponse,
    WatermarkCreate, WatermarkResponse,
    ApplyWatermarkRequest, ForensicRequest, ForensicResponse,
    TraceRequest, TraceResponse
)
from app.services.watermark_service import WatermarkService
from app.middleware.tenant import get_tenant_id

router = APIRouter(prefix="/watermarks", tags=["watermarks"])


@router.post("/config", response_model=WatermarkConfigResponse)
async def configure_watermark(
    config: WatermarkConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    return await service.configure_watermark(
        tenant_id=tenant_id,
        default_type=config.default_type,
        default_position=config.default_position,
        default_opacity=config.default_opacity,
        default_scale=config.default_scale,
        custom_x=config.custom_x,
        custom_y=config.custom_y,
        forensic_enabled=config.forensic_enabled,
        forensic_strength=config.forensic_strength,
        user_watermark_enabled=config.user_watermark_enabled,
    )


@router.get("/config", response_model=WatermarkConfigResponse)
async def get_watermark_config(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    config = await service.get_configuration(tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="Watermark configuration not found")
    return config


@router.post("", response_model=WatermarkResponse)
async def create_watermark(
    watermark: WatermarkCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    return await service.create_watermark(
        tenant_id=tenant_id,
        name=watermark.name,
        type=watermark.type,
        image_path=watermark.image_path,
        text_content=watermark.text_content,
        position=watermark.position,
        opacity=watermark.opacity,
        scale=watermark.scale,
        custom_x=watermark.custom_x,
        custom_y=watermark.custom_y,
        font_size=watermark.font_size,
        font_color=watermark.font_color,
    )


@router.get("", response_model=List[WatermarkResponse])
async def list_watermarks(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    return await service.list_watermarks(tenant_id)


@router.post("/apply")
async def apply_watermark(
    request: ApplyWatermarkRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    session = await service.apply_watermark(
        tenant_id=tenant_id,
        user_id=current_user.id,
        content_id=request.content_id,
        content_type=request.content_type,
        session_id=request.session_id,
        watermark_id=request.watermark_id,
        user_specific_text=request.user_specific_text,
    )
    return {"session_id": session.id, "watermark_data": session.watermark_data}


@router.post("/forensic", response_model=ForensicResponse)
async def generate_forensic(
    request: ForensicRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    config = await service.get_configuration(tenant_id)
    
    if not config or not config.forensic_enabled:
        raise HTTPException(status_code=403, detail="Forensic watermarking not enabled")
    
    forensic = await service.generate_forensic(
        tenant_id=tenant_id,
        user_id=current_user.id,
        content_id=request.content_id,
        content_type=request.content_type,
        session_id=request.session_id,
        strength=request.strength,
        ip_address=req.client.host if req.client else None,
    )
    
    return ForensicResponse(
        pattern_id=forensic.pattern_id,
        embedded_data=forensic.embedded_data,
        content_id=forensic.content_id,
        created_at=forensic.created_at,
    )


@router.post("/trace", response_model=TraceResponse)
async def trace_leak(
    request: TraceRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = WatermarkService(db)
    trace = await service.trace_leak(
        tenant_id=tenant_id,
        sample_data=request.sample_data,
        content_id=request.content_id,
    )
    
    if trace:
        return TraceResponse(
            found=True,
            source_user_id=trace.source_user_id,
            source_session_id=trace.source_session_id,
            confidence_score=trace.confidence_score,
            trace_id=trace.id,
        )
    
    return TraceResponse(
        found=False,
        source_user_id=None,
        source_session_id=None,
        confidence_score=0.0,
        trace_id=0,
    )
