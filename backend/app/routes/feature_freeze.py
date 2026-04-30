from fastapi import APIRouter
from typing import Dict, Any
from app.services.feature_freeze import feature_freeze_service

router = APIRouter(prefix="/api/freeze", tags=["feature-freeze"])

@router.post("/audit")
async def audit() -> Dict[str, Any]:
    return await feature_freeze_service.audit_features()

@router.post("/lock-flags")
async def lock_flags() -> Dict[str, Any]:
    return await feature_freeze_service.lock_feature_flags()

@router.post("/cleanup")
async def cleanup() -> Dict[str, Any]:
    return await feature_freeze_service.cleanup_toggles()

@router.get("/checklist")
async def checklist() -> Dict[str, Any]:
    return await feature_freeze_service.create_checklist()

@router.post("/document")
async def document() -> Dict[str, Any]:
    return await feature_freeze_service.document_features()
