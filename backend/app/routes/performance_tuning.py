from fastapi import APIRouter
from typing import Dict, Any
from app.services.performance_tuning import performance_tuning_service

router = APIRouter(prefix="/api/performance", tags=["performance"])

@router.post("/queries/optimize")
async def optimize_queries() -> Dict[str, Any]:
    return await performance_tuning_service.optimize_queries()

@router.get("/caching")
async def get_caching() -> Dict[str, Any]:
    return await performance_tuning_service.refine_caching()

@router.get("/resources")
async def get_resources() -> Dict[str, Any]:
    return await performance_tuning_service.optimize_resources()

@router.get("/latency")
async def get_latency() -> Dict[str, Any]:
    return await performance_tuning_service.reduce_latency()

@router.post("/load-test")
async def run_load_test() -> Dict[str, Any]:
    return await performance_tuning_service.run_load_test()
