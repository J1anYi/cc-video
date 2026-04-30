from fastapi import APIRouter
from typing import Dict, Any
from app.services.multi_tenant import multi_tenant_service

router = APIRouter(prefix="/api/tenants", tags=["multi-tenant"])

@router.post("/")
async def create_tenant(name: str, schema: str) -> Dict[str, Any]:
    return await multi_tenant_service.create_tenant(name, schema)

@router.get("/{tenant_id}")
async def get_tenant(tenant_id: str) -> Dict[str, Any]:
    return await multi_tenant_service.get_tenant(tenant_id)

@router.get("/")
async def list_tenants() -> Dict[str, Any]:
    return await multi_tenant_service.list_tenants()

@router.put("/{tenant_id}")
async def update_tenant(tenant_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return await multi_tenant_service.update_tenant(tenant_id, data)

@router.delete("/{tenant_id}")
async def delete_tenant(tenant_id: str) -> Dict[str, Any]:
    return await multi_tenant_service.delete_tenant(tenant_id)

@router.get("/{tenant_id}/config")
async def get_config(tenant_id: str) -> Dict[str, Any]:
    return await multi_tenant_service.get_tenant_config(tenant_id)

@router.get("/{tenant_id}/billing")
async def get_billing(tenant_id: str) -> Dict[str, Any]:
    return await multi_tenant_service.get_billing(tenant_id)
