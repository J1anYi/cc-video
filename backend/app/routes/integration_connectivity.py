from fastapi import APIRouter
from typing import Dict, Any
from app.services.integration_connectivity import integration_connectivity_service

router = APIRouter(prefix="/api/integration", tags=["integration"])

@router.post("/calendar/{tenant_id}")
async def integrate_calendar(tenant_id: str, provider: str) -> Dict[str, Any]:
    return await integration_connectivity_service.integrate_calendar(tenant_id, provider)

@router.post("/sso/{tenant_id}")
async def enhance_sso(tenant_id: str, provider: str) -> Dict[str, Any]:
    return await integration_connectivity_service.enhance_sso(tenant_id, provider)

@router.post("/webhooks/{tenant_id}")
async def setup_webhooks(tenant_id: str) -> Dict[str, Any]:
    return await integration_connectivity_service.setup_webhooks(tenant_id)

@router.post("/content-api/{tenant_id}")
async def extend_content_api(tenant_id: str) -> Dict[str, Any]:
    return await integration_connectivity_service.extend_content_api(tenant_id)

@router.post("/mobile-sync/{tenant_id}")
async def sync_mobile_framework(tenant_id: str) -> Dict[str, Any]:
    return await integration_connectivity_service.sync_mobile_framework(tenant_id)
