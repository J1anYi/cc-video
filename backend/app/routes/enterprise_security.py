from fastapi import APIRouter
from typing import Dict, Any
from app.services.enterprise_security import enterprise_security_service

router = APIRouter(prefix="/api/enterprise-security", tags=["enterprise-security"])

@router.get("/compliance")
async def get_compliance() -> Dict[str, Any]:
    return await enterprise_security_service.get_compliance_status()

@router.post("/export-data/{user_id}")
async def export_data(user_id: str) -> Dict[str, Any]:
    return await enterprise_security_service.export_user_data(user_id)

@router.delete("/delete-data/{user_id}")
async def delete_data(user_id: str) -> Dict[str, Any]:
    return await enterprise_security_service.delete_user_data(user_id)

@router.get("/rbac/{role_id}")
async def get_rbac(role_id: str) -> Dict[str, Any]:
    return await enterprise_security_service.get_rbac_permissions(role_id)

@router.post("/sso/{provider}")
async def configure_sso(provider: str) -> Dict[str, Any]:
    return await enterprise_security_service.configure_sso(provider)
