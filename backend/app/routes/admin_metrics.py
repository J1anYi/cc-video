from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.services.content_metrics import content_metrics_service

router = APIRouter(prefix="/api/admin/metrics", tags=["admin-metrics"])


@router.get("/overview")
async def get_metrics_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get platform-wide metrics overview."""
    return await content_metrics_service.get_platform_overview(db)


@router.get("/movies/{movie_id}")
async def get_movie_metrics(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get performance metrics for a specific movie."""
    return await content_metrics_service.get_movie_metrics(db, movie_id)


@router.get("/trending")
async def get_trending_content(
    period: str = Query("week", description="Period: week, month, or all"),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get top performing content."""
    return await content_metrics_service.get_trending_content(db, period, limit)


@router.get("/retention")
async def get_retention_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get user retention metrics."""
    return await content_metrics_service.get_retention_metrics(db)


@router.get("/rankings")
async def get_content_rankings(
    sort_by: str = Query("views", description="Sort by: views, rating, or recent"),
    genre: str = Query(None, description="Filter by genre"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get content rankings."""
    return await content_metrics_service.get_content_rankings(db, sort_by, genre, limit)
