from fastapi import APIRouter, Depends, Query, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_db, require_admin
from app.schemas.content_analytics import (
    ContentMetricsResponse,
    HeatmapResponse,
    CompletionAnalysisResponse,
    ContentComparisonResponse,
    TrendingContentResponse,
)
from app.services.content_analytics_service import content_analytics_service

router = APIRouter(prefix="/admin/content", tags=["content-analytics"])


@router.get("/analytics/trending", response_model=TrendingContentResponse)
async def get_trending_content(
    limit: int = Query(20, ge=1, le=100),
    time_range: str = Query("24h", description="Time range: 24h, 7d, 30d"),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get trending content with velocity metrics."""
    content = await content_analytics_service.get_trending_content(db, limit, time_range)
    from datetime import datetime
    return {
        "content": content,
        "time_range": time_range,
        "generated_at": datetime.utcnow().isoformat(),
    }


@router.get("/{content_id}/analytics", response_model=ContentMetricsResponse)
async def get_content_metrics(
    content_id: int,
    refresh: bool = Query(False, description="Force refresh metrics"),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get analytics for a specific content item."""
    metrics = await content_analytics_service.get_content_metrics(db, content_id, refresh)
    return ContentMetricsResponse(**metrics)


@router.get("/{content_id}/heatmap", response_model=HeatmapResponse)
async def get_content_heatmap(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get engagement heatmap for a content item."""
    heatmap = await content_analytics_service.get_engagement_heatmap(db, content_id)
    return HeatmapResponse(**heatmap)


@router.get("/{content_id}/completion", response_model=CompletionAnalysisResponse)
async def get_completion_analysis(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get completion analysis for a content item."""
    analysis = await content_analytics_service.compute_completion_analysis(db, content_id)
    return CompletionAnalysisResponse(**analysis)


@router.post("/compare", response_model=ContentComparisonResponse)
async def compare_content(
    content_ids: List[int] = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Compare analytics across multiple content items."""
    if len(content_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least 2 content IDs required for comparison"
        )
    if len(content_ids) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 content IDs allowed for comparison"
        )

    items = await content_analytics_service.compare_content(db, content_ids)
    return ContentComparisonResponse(items=items)
