from fastapi import APIRouter
from typing import Dict, Any
from app.services.performance_validation import performance_validation_service

router = APIRouter(prefix="/api/performance-validation", tags=["performance-validation"])

@router.post("/load-suite")
async def load_suite() -> Dict[str, Any]:
    return await performance_validation_service.create_load_suite()

@router.post("/benchmarks")
async def benchmarks() -> Dict[str, Any]:
    return await performance_validation_service.create_benchmarks()

@router.post("/monitoring")
async def monitoring() -> Dict[str, Any]:
    return await performance_validation_service.add_monitoring()

@router.post("/optimization")
async def optimization() -> Dict[str, Any]:
    return await performance_validation_service.implement_optimization()

@router.post("/incident-response")
async def incident_response() -> Dict[str, Any]:
    return await performance_validation_service.create_incident_response()
