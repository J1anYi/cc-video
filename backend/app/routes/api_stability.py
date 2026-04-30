from fastapi import APIRouter
from typing import Dict, Any
from app.services.api_stability import api_stability_service

router = APIRouter(prefix="/api/stability", tags=["api-stability"])

@router.post("/versioning")
async def versioning() -> Dict[str, Any]:
    return await api_stability_service.implement_versioning()

@router.post("/compatibility")
async def compatibility() -> Dict[str, Any]:
    return await api_stability_service.create_compatibility_layer()

@router.post("/contract-testing")
async def contract_testing() -> Dict[str, Any]:
    return await api_stability_service.add_contract_testing()

@router.post("/rate-limiting")
async def rate_limiting() -> Dict[str, Any]:
    return await api_stability_service.implement_rate_limiting()

@router.post("/documentation")
async def documentation() -> Dict[str, Any]:
    return await api_stability_service.create_documentation()
