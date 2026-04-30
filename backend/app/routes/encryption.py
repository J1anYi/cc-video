"""Content encryption API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.encryption import EncryptionAlgorithm
from app.schemas.encryption import (
    EncryptionConfigCreate, EncryptionConfigResponse,
    EncryptionKeyCreate, EncryptionKeyResponse,
    KeyDeliveryRequest, KeyDeliveryResponse,
    EncryptionStatusResponse
)
from app.services.encryption_service import EncryptionService
from app.middleware.tenant import get_tenant_id
from app.routes.auth import get_current_user

router = APIRouter(prefix="/encryption", tags=["encryption"])


@router.post("/config", response_model=EncryptionConfigResponse)
async def configure_encryption(config: EncryptionConfigCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = EncryptionService(db)
    return await service.configure_encryption(tenant_id=tenant_id, algorithm=config.algorithm, key_rotation_days=config.key_rotation_days, encryption_at_rest=config.encryption_at_rest, end_to_end_encryption=config.end_to_end_encryption, secure_key_delivery=config.secure_key_delivery, key_delivery_ttl_seconds=config.key_delivery_ttl_seconds)


@router.get("/config", response_model=EncryptionConfigResponse)
async def get_encryption_config(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = EncryptionService(db)
    config = await service.get_configuration(tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="Encryption configuration not found")
    return config


@router.post("/keys", response_model=EncryptionKeyResponse)
async def generate_key(key: EncryptionKeyCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = EncryptionService(db)
    config = await service.get_configuration(tenant_id)
    return await service.generate_key(tenant_id=tenant_id, content_id=key.content_id, content_type=key.content_type, algorithm=key.algorithm, key_rotation_days=config.key_rotation_days if config else 30)


@router.post("/deliver", response_model=KeyDeliveryResponse)
async def deliver_key(request: KeyDeliveryRequest, req: Request, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = EncryptionService(db)
    config = await service.get_configuration(tenant_id)
    ttl = config.key_delivery_ttl_seconds if config else 3600
    key, delivery_token, expires_at = await service.deliver_key(tenant_id=tenant_id, user_id=current_user.id, content_id=request.content_id, content_type=request.content_type, session_id=request.session_id, device_id=request.device_id, ip_address=req.client.host if req.client else None, ttl_seconds=ttl)
    return KeyDeliveryResponse(delivery_token=delivery_token, key_id=key.key_id, algorithm=key.algorithm, expires_at=expires_at)


@router.get("/status/{content_id}", response_model=EncryptionStatusResponse)
async def get_encryption_status(content_id: int, content_type: str = "movie", db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = EncryptionService(db)
    is_encrypted, algorithm, key_status, last_rotated = await service.get_encryption_status(tenant_id, content_id, content_type)
    return EncryptionStatusResponse(content_id=content_id, content_type=content_type, is_encrypted=is_encrypted, algorithm=algorithm, key_status=key_status, last_rotated=last_rotated)
