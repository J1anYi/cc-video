from fastapi import APIRouter
from typing import Dict, Any
from app.services.api_consolidation import api_consolidation_service

router = APIRouter(prefix="/api/consolidation", tags=["api-consolidation"])

@router.get("/deprecated")
async def list_deprecated() -> Dict[str, Any]:
    endpoints = await api_consolidation_service.identify_deprecated_endpoints()
    return {"deprecated": endpoints}

@router.post("/deprecate")
async def apply_deprecations() -> Dict[str, Any]:
    return await api_consolidation_service.apply_deprecations()

@router.get("/migration-guide")
async def get_migration_guide() -> Dict[str, Any]:
    return await api_consolidation_service.create_migration_guide()

@router.get("/docs")
async def get_docs() -> Dict[str, Any]:
    return await api_consolidation_service.generate_consolidated_docs()

@router.get("/sdk/migration")
async def get_sdk_guide() -> Dict[str, Any]:
    return await api_consolidation_service.generate_sdk_migration_guide()

@router.get("/performance")
async def get_performance() -> Dict[str, Any]:
    return await api_consolidation_service.analyze_performance()
