"""Access control API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models.access import PermissionType
from app.schemas.access import (
    AccessPolicyCreate, AccessPolicyResponse,
    ContentPermissionCreate, ContentPermissionResponse,
    AccessCheckRequest, AccessCheckResponse,
    StreamSessionResponse
)
from app.services.access_service import AccessControlService
from app.middleware.tenant import get_tenant_id
from app.routes.auth import get_current_user

router = APIRouter(prefix="/access", tags=["access"])


@router.post("/policies", response_model=AccessPolicyResponse)
async def create_policy(policy: AccessPolicyCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = AccessControlService(db)
    return await service.create_policy(tenant_id=tenant_id, name=policy.name, description=policy.description, default_level=policy.default_level, max_devices=policy.max_devices, max_concurrent_streams=policy.max_concurrent_streams)


@router.get("/policies", response_model=List[AccessPolicyResponse])
async def list_policies(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = AccessControlService(db)
    return await service.list_policies(tenant_id)


@router.post("/permissions", response_model=ContentPermissionResponse)
async def set_permission(perm: ContentPermissionCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = AccessControlService(db)
    return await service.set_permission(tenant_id=tenant_id, content_id=perm.content_id, content_type=perm.content_type, granted_by=current_user.id, user_id=perm.user_id, role_id=perm.role_id, permission_type=perm.permission_type, access_level=perm.access_level, expires_at=perm.expires_at)


@router.post("/check", response_model=AccessCheckResponse)
async def check_access(request: AccessCheckRequest, req: Request, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = AccessControlService(db)
    allowed, access_level, reason, session_token = await service.check_access(tenant_id=tenant_id, user_id=current_user.id, content_id=request.content_id, content_type=request.content_type, device_id=request.device_id, permission_type=request.permission_type, ip_address=req.client.host if req.client else None)
    return AccessCheckResponse(allowed=allowed, access_level=access_level, reason=reason, session_token=session_token)


@router.get("/sessions", response_model=List[StreamSessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = AccessControlService(db)
    return await service.list_sessions(tenant_id, current_user.id)


@router.delete("/sessions/{session_id}")
async def terminate_session(session_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = AccessControlService(db)
    success = await service.terminate_session(tenant_id, current_user.id, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"success": True}
