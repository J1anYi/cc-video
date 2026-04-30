"""DRM API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.drm import DRMProvider, DeviceType
from app.schemas.drm import (
    DRMConfigCreate, DRMConfigResponse,
    DRMKeyCreate, DRMKeyResponse,
    LicenseRequest, LicenseResponse,
    DeviceRegisterRequest, DeviceResponse,
    OfflineTokenRequest, OfflineTokenResponse,
    KeyRotationRequest, KeyRotationResponse
)
from app.services.drm_service import DRMService
from app.middleware.tenant import get_tenant_id

router = APIRouter(prefix="/drm", tags=["drm"])


@router.post("/config", response_model=DRMConfigResponse)
async def configure_drm(
    config: DRMConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    return await service.configure_drm(
        tenant_id=tenant_id,
        provider=config.provider,
        widevine_license_url=config.widevine_license_url,
        widevine_provider_id=config.widevine_provider_id,
        playready_license_url=config.playready_license_url,
        playready_key_id=config.playready_key_id,
        fairplay_license_url=config.fairplay_license_url,
        fairplay_cert_url=config.fairplay_cert_url,
        max_devices_per_user=config.max_devices_per_user,
        offline_playback_enabled=config.offline_playback_enabled,
        offline_duration_hours=config.offline_duration_hours,
        key_rotation_days=config.key_rotation_days,
    )


@router.get("/config", response_model=DRMConfigResponse)
async def get_drm_config(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    config = await service.get_configuration(tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="DRM configuration not found")
    return config


@router.post("/keys", response_model=DRMKeyResponse)
async def generate_content_key(
    key: DRMKeyCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    return await service.generate_content_key(
        tenant_id=tenant_id,
        content_id=key.content_id,
        content_type=key.content_type,
        provider=key.provider,
    )


@router.post("/license", response_model=LicenseResponse)
async def issue_license(
    request: LicenseRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    config = await service.get_configuration(tenant_id)
    license, key = await service.issue_license(
        tenant_id=tenant_id,
        user_id=current_user.id,
        content_id=request.content_id,
        content_type=request.content_type,
        device_id=request.device_id,
        provider=request.provider,
    )
    return LicenseResponse(
        license_token=license.license_token,
        key_id=key.key_id,
        provider=license.provider,
        content_id=license.content_id,
        issued_at=license.issued_at,
        expires_at=license.expires_at,
    )


@router.post("/devices", response_model=DeviceResponse)
async def register_device(
    request: DeviceRegisterRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    config = await service.get_configuration(tenant_id)
    max_devices = config.max_devices_per_user if config else 5
    
    return await service.register_device(
        tenant_id=tenant_id,
        user_id=current_user.id,
        device_id=request.device_id,
        device_name=request.device_name,
        device_type=request.device_type,
        drm_provider=request.drm_provider,
        user_agent=req.headers.get("user-agent"),
        ip_address=req.client.host if req.client else None,
        max_devices=max_devices,
    )


@router.get("/devices", response_model=List[DeviceResponse])
async def list_devices(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    return await service.list_devices(tenant_id, current_user.id)


@router.delete("/devices/{device_id}")
async def remove_device(
    device_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    success = await service.remove_device(tenant_id, current_user.id, device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"success": True}


@router.post("/offline-token", response_model=OfflineTokenResponse)
async def generate_offline_token(
    request: OfflineTokenRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    config = await service.get_configuration(tenant_id)
    
    if not config or not config.offline_playback_enabled:
        raise HTTPException(status_code=403, detail="Offline playback not enabled")
    
    token, key = await service.generate_offline_token(
        tenant_id=tenant_id,
        user_id=current_user.id,
        content_id=request.content_id,
        content_type=request.content_type,
        device_id=request.device_id,
        provider=request.provider,
        duration_hours=config.offline_duration_hours,
    )
    
    return OfflineTokenResponse(
        token=token.token,
        content_id=token.content_id,
        device_id=token.device_id,
        expires_at=token.expires_at,
        encrypted_key=token.encrypted_key,
    )


@router.post("/rotate-keys", response_model=KeyRotationResponse)
async def rotate_keys(
    request: KeyRotationRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = DRMService(db)
    old_key, new_key = await service.rotate_keys(
        tenant_id=tenant_id,
        content_id=request.content_id,
        content_type=request.content_type,
    )
    
    return KeyRotationResponse(
        old_key_id=old_key.key_id if old_key else "",
        new_key_id=new_key.key_id,
        rotated_at=new_key.created_at,
    )
