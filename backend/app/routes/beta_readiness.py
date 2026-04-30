from fastapi import APIRouter
from typing import Dict, Any
from app.services.beta_readiness import beta_readiness_service

router = APIRouter(prefix="/api/beta", tags=["beta-readiness"])

@router.post("/infrastructure")
async def infrastructure() -> Dict[str, Any]:
    return await beta_readiness_service.setup_infrastructure()

@router.post("/onboarding")
async def onboarding() -> Dict[str, Any]:
    return await beta_readiness_service.create_onboarding()

@router.post("/access-controls")
async def access_controls() -> Dict[str, Any]:
    return await beta_readiness_service.implement_access_controls()

@router.post("/analytics")
async def analytics() -> Dict[str, Any]:
    return await beta_readiness_service.add_analytics()

@router.post("/procedures")
async def procedures() -> Dict[str, Any]:
    return await beta_readiness_service.create_procedures()
