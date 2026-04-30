"""Phase 204: Data Residency Routes"""
from fastapi import APIRouter, Body
from typing import List
from ..services.data_residency import DataResidencyService

router = APIRouter(prefix="/api/data-residency", tags=["data-residency"])
service = DataResidencyService()

@router.post("/manage/{tenant_id}")
async def manage_residency(tenant_id: str, regions: List[str] = Body(default=[])):
    return await service.manage_data_residency(tenant_id, regions)

@router.post("/compliance/{tenant_id}")
async def setup_comp(tenant_id: str, regulations: List[str] = Body(default=[])):
    return await service.setup_compliance(tenant_id, regulations)

@router.post("/ratings/{content_id}")
async def manage_rat(content_id: str, ratings: dict):
    return await service.manage_ratings(content_id, ratings)

@router.post("/takedowns/{content_id}")
async def manage_take(content_id: str, request: dict):
    return await service.manage_takedowns(content_id, request)

@router.get("/report/{tenant_id}")
async def get_report(tenant_id: str):
    return await service.get_compliance_report(tenant_id)
