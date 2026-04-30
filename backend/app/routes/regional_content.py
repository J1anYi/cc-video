"""Phase 202: Regional Content Routes"""
from fastapi import APIRouter
from ..services.regional_content import RegionalContentService

router = APIRouter(prefix="/api/regional-content", tags=["regional-content"])
service = RegionalContentService()

@router.post("/geo/{content_id}")
async def manage_geo(content_id: str, restrictions: dict):
    return await service.manage_geo_restrictions(content_id, restrictions)

@router.post("/partnerships/{region}")
async def manage_partners(region: str, partnership_data: dict):
    return await service.manage_partnerships(region, partnership_data)

@router.post("/windowing/{content_id}")
async def manage_window(content_id: str, window_config: dict):
    return await service.manage_windowing(content_id, window_config)

@router.post("/curate/{region}")
async def curate(region: str, curation_data: dict):
    return await service.curate_regional(region, curation_data)

@router.get("/analytics/{content_id}")
async def get_analytics(content_id: str):
    return await service.get_licensing_analytics(content_id)
