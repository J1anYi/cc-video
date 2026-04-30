"""Phase 205: Global Infrastructure Routes"""
from fastapi import APIRouter, Body
from typing import List
from ..services.global_infrastructure import GlobalInfrastructureService

router = APIRouter(prefix="/api/global-infrastructure", tags=["global-infrastructure"])
service = GlobalInfrastructureService()

@router.post("/multi-region/{tenant_id}")
async def setup_multi(tenant_id: str, regions: List[str] = Body(default=[])):
    return await service.setup_multi_region(tenant_id, regions)

@router.get("/monitor/{region}")
async def monitor(region: str):
    return await service.monitor_performance(region)

@router.post("/disaster-recovery/{tenant_id}")
async def setup_dr(tenant_id: str):
    return await service.setup_disaster_recovery(tenant_id)

@router.post("/support/{region}")
async def setup_sup(region: str, config: dict):
    return await service.setup_regional_support(region, config)

@router.post("/launch/{market}")
async def prepare(market: str, checklist: dict):
    return await service.prepare_launch(market, checklist)
