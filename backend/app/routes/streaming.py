"""Streaming routes for adaptive bitrate."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user, get_current_user_optional
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.services.streaming_service import StreamingService
from app.models.streaming import QualityLevel


router = APIRouter(prefix="/streaming", tags=["streaming"])


class VariantCreate(BaseModel):
    movie_id: int
    quality: str
    resolution: str
    bitrate: int
    hls_url: str
    manifest_url: Optional[str] = None
    file_size: int = 0


class MetricCreate(BaseModel):
    bandwidth_kbps: int
    quality_selected: Optional[str] = None
    quality_played: Optional[str] = None
    movie_id: Optional[int] = None
    buffer_events: int = 0
    rebuffer_time_ms: int = 0


class PreferenceUpdate(BaseModel):
    preferred_quality: str
    auto_adjust: bool = True
    limit_mobile_data: bool = False


@router.post("/variants")
async def create_variant(
    data: VariantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = StreamingService(db)
    try:
        quality_enum = QualityLevel(data.quality)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quality level")
    
    variant = await service.create_stream_variant(
        movie_id=data.movie_id,
        tenant_id=tenant_id,
        quality=quality_enum,
        resolution=data.resolution,
        bitrate=data.bitrate,
        hls_url=data.hls_url,
        manifest_url=data.manifest_url,
        file_size=data.file_size,
    )
    return {"id": variant.id, "quality": variant.quality.value}


@router.get("/movies/{movie_id}/variants")
async def get_movie_variants(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    service = StreamingService(db)
    variants = await service.get_variants_for_movie(movie_id, tenant_id)
    return {
        "variants": [
            {
                "id": v.id,
                "quality": v.quality.value,
                "resolution": v.resolution,
                "bitrate": v.bitrate,
                "hls_url": v.hls_url,
                "manifest_url": v.manifest_url,
            }
            for v in variants
        ]
    }


@router.post("/metrics")
async def record_metric(
    data: MetricCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    tenant_id: int = Depends(get_tenant_id),
):
    service = StreamingService(db)
    
    quality_selected = QualityLevel(data.quality_selected) if data.quality_selected else None
    quality_played = QualityLevel(data.quality_played) if data.quality_played else None
    
    metric = await service.record_bandwidth_metric(
        tenant_id=tenant_id,
        bandwidth_kbps=data.bandwidth_kbps,
        quality_selected=quality_selected,
        quality_played=quality_played,
        user_id=current_user.id if current_user else None,
        movie_id=data.movie_id,
        buffer_events=data.buffer_events,
        rebuffer_time_ms=data.rebuffer_time_ms,
    )
    return {"id": metric.id}


@router.get("/stats")
async def get_bandwidth_stats(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    service = StreamingService(db)
    stats = await service.get_bandwidth_stats(tenant_id)
    return stats


@router.get("/recommend")
async def recommend_quality(
    bandwidth_kbps: int = Query(..., ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = StreamingService(db)
    quality = await service.get_recommended_quality(bandwidth_kbps)
    return {"recommended_quality": quality.value}


@router.get("/preferences")
async def get_preferences(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = StreamingService(db)
    pref = await service.get_quality_preference(current_user.id)
    if not pref:
        return {"preferred_quality": "auto", "auto_adjust": True, "limit_mobile_data": False}
    return {
        "preferred_quality": pref.preferred_quality.value,
        "auto_adjust": pref.auto_adjust,
        "limit_mobile_data": pref.limit_mobile_data,
    }


@router.put("/preferences")
async def update_preferences(
    data: PreferenceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = StreamingService(db)
    try:
        quality_enum = QualityLevel(data.preferred_quality)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid quality level")
    
    pref = await service.set_quality_preference(
        user_id=current_user.id,
        tenant_id=tenant_id,
        preferred_quality=quality_enum,
        auto_adjust=data.auto_adjust,
        limit_mobile_data=data.limit_mobile_data,
    )
    return {"preferred_quality": pref.preferred_quality.value}
