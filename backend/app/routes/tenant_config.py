from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import json

from app.dependencies import get_db, require_admin, get_current_user
from app.models.user import User
from app.models.tenant import Tenant
from sqlalchemy import select


router = APIRouter(prefix="/tenant-config", tags=["tenant-config"])


class TenantConfig(BaseModel):
    features: dict = {}
    storage_limit_gb: Optional[int] = None
    bandwidth_limit_gb: Optional[int] = None
    auth_providers: list = []
    moderation_rules: dict = {}
    notification_preferences: dict = {}


@router.get("/", response_model=TenantConfig)
async def get_tenant_config(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TenantConfig:
    if not current_user.tenant_id:
        return TenantConfig()
    
    result = await db.execute(select(Tenant).where(Tenant.id == current_user.tenant_id))
    tenant = result.scalar_one_or_none()
    
    if not tenant or not tenant.settings:
        return TenantConfig()
    
    settings = json.loads(tenant.settings)
    return TenantConfig(
        features=settings.get("features", {}),
        storage_limit_gb=settings.get("storage_limit_gb"),
        bandwidth_limit_gb=settings.get("bandwidth_limit_gb"),
        auth_providers=settings.get("auth_providers", []),
        moderation_rules=settings.get("moderation_rules", {}),
        notification_preferences=settings.get("notification_preferences", {}),
    )


@router.put("/", response_model=TenantConfig)
async def update_tenant_config(
    config: TenantConfig,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> TenantConfig:
    if not admin.tenant_id:
        raise HTTPException(status_code=400, detail="No tenant context")
    
    result = await db.execute(select(Tenant).where(Tenant.id == admin.tenant_id))
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    current_settings = json.loads(tenant.settings) if tenant.settings else {}
    
    current_settings.update({
        "features": config.features,
        "storage_limit_gb": config.storage_limit_gb,
        "bandwidth_limit_gb": config.bandwidth_limit_gb,
        "auth_providers": config.auth_providers,
        "moderation_rules": config.moderation_rules,
        "notification_preferences": config.notification_preferences,
    })
    
    tenant.settings = json.dumps(current_settings)
    await db.commit()
    
    return config
