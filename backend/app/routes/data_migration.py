from fastapi import APIRouter
from typing import Dict, Any
from app.services.data_migration import data_migration_service

router = APIRouter(prefix="/api/migration", tags=["data-migration"])

@router.get("/legacy")
async def get_legacy() -> Dict[str, Any]:
    return await data_migration_service.identify_legacy_data()

@router.post("/cleanup/{table}")
async def cleanup(table: str) -> Dict[str, Any]:
    return await data_migration_service.cleanup_legacy_data(table)

@router.get("/schema/analyze")
async def analyze() -> Dict[str, Any]:
    return await data_migration_service.analyze_schema()

@router.post("/schema/optimize/{table}")
async def optimize(table: str) -> Dict[str, Any]:
    return await data_migration_service.optimize_schema(table)

@router.get("/validate")
async def validate() -> Dict[str, Any]:
    return await data_migration_service.validate_data_integrity()
