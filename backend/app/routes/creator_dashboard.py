"""Phase 196: Creator Dashboard Routes"""
from fastapi import APIRouter
from ..services.creator_dashboard import CreatorDashboardService

router = APIRouter(prefix="/api/creator-dashboard", tags=["creator-dashboard"])
service = CreatorDashboardService()

@router.get("/{creator_id}")
async def get_dashboard(creator_id: str):
    return await service.get_creator_dashboard(creator_id)

@router.get("/{creator_id}/analytics")
async def get_analytics(creator_id: str):
    return await service.get_realtime_analytics(creator_id)

@router.get("/{creator_id}/revenue")
async def get_revenue(creator_id: str):
    return await service.get_revenue_dashboard(creator_id)

@router.get("/{creator_id}/audience")
async def get_audience(creator_id: str):
    return await service.get_audience_insights(creator_id)

@router.get("/{creator_id}/alerts")
async def get_alerts(creator_id: str):
    return await service.get_performance_alerts(creator_id)
