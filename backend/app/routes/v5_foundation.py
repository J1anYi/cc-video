from fastapi import APIRouter
from typing import Dict, Any
from app.services.v5_foundation import v5_foundation_service

router = APIRouter(prefix="/api/v5-foundation", tags=["v5-foundation"])

@router.get("/architecture")
async def review_architecture() -> Dict[str, Any]:
    return await v5_foundation_service.review_architecture()

@router.get("/stack")
async def evaluate_stack() -> Dict[str, Any]:
    return await v5_foundation_service.evaluate_stack()

@router.get("/scalability")
async def assess_scalability() -> Dict[str, Any]:
    return await v5_foundation_service.assess_scalability()

@router.get("/deprecations")
async def plan_deprecations() -> Dict[str, Any]:
    return await v5_foundation_service.plan_deprecations()

@router.get("/roadmap")
async def define_roadmap() -> Dict[str, Any]:
    return await v5_foundation_service.define_roadmap()
