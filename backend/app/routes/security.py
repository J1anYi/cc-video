from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import require_admin, get_current_user
from app.services.security_service import security_service

router = APIRouter(prefix="/security", tags=["Security"])


class TwoFactorVerify(BaseModel):
    code: str


@router.post("/2fa/enable")
async def enable_2fa(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    tfa = await security_service.enable_2fa(db, user.id)
    return {"enabled": True, "secret": tfa.secret}


@router.post("/2fa/verify")
async def verify_2fa(data: TwoFactorVerify, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    valid = await security_service.verify_2fa(db, user.id, data.code)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid 2FA code")
    return {"verified": True}


@router.post("/2fa/disable")
async def disable_2fa(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    tfa = await security_service.disable_2fa(db, user.id)
    return {"enabled": False}


@router.get("/2fa")
async def get_2fa_status(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    tfa = await security_service.get_2fa(db, user.id)
    return {"enabled": tfa.is_enabled if tfa else False}


@router.get("/audit-logs")
async def get_audit_logs(
    limit: int = 100,
    action: str = None,
    db: AsyncSession = Depends(get_db),
    admin=Depends(require_admin),
    request: Request = None,
):
    tenant_id = getattr(request.state, "tenant_id", None) if request else None
    logs = await security_service.get_audit_logs(db, tenant_id=tenant_id, action=action, limit=limit)
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]


@router.post("/audit-logs")
async def create_audit_log(
    action: str,
    resource_type: str = None,
    resource_id: int = None,
    details: dict = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    request: Request = None,
):
    tenant_id = getattr(request.state, "tenant_id", None) if request else None
    ip = request.client.host if request else None
    ua = request.headers.get("user-agent") if request else None
    
    log = await security_service.log_action(
        db, action=action, user_id=user.id, tenant_id=tenant_id,
        resource_type=resource_type, resource_id=resource_id,
        details=details, ip_address=ip, user_agent=ua
    )
    return {"id": log.id, "action": log.action}


@router.post("/gdpr/export")
async def export_user_data(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    data = await security_service.export_user_data(db, user.id)
    await security_service.request_data_export(db, user.id)
    return data


@router.post("/gdpr/deletion-request")
async def request_data_deletion(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    request = await security_service.request_data_deletion(db, user.id)
    return {"request_id": request.id, "status": request.status}
