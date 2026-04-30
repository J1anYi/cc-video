from fastapi import APIRouter
from typing import Dict, Any
from app.services.perf_optimization import perf_optimization_service

router = APIRouter(prefix="/api/perf-opt", tags=["perf-optimization"])

@router.post("/queries/{tenant_id}")
async def optimize_queries(tenant_id: str) -> Dict[str, Any]:
    return await perf_optimization_service.optimize_queries(tenant_id)

@router.post("/abr/{video_id}")
async def improve_abr(video_id: str) -> Dict[str, Any]:
    return await perf_optimization_service.improve_abr(video_id)

@router.post("/sync/{room_id}")
async def reduce_latency(room_id: str) -> Dict[str, Any]:
    return await perf_optimization_service.reduce_sync_latency(room_id)

@router.post("/ai/{model_id}")
async def optimize_ai(model_id: str) -> Dict[str, Any]:
    return await perf_optimization_service.optimize_ai_response(model_id)

@router.post("/pool/{tenant_id}")
async def pool_connections(tenant_id: str) -> Dict[str, Any]:
    return await perf_optimization_service.pool_connections(tenant_id)
