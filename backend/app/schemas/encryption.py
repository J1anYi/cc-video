"""Content encryption schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.encryption import EncryptionAlgorithm, KeyStatus


class EncryptionConfigCreate(BaseModel):
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM
    key_rotation_days: int = 30
    encryption_at_rest: bool = True
    end_to_end_encryption: bool = False
    secure_key_delivery: bool = True
    key_delivery_ttl_seconds: int = 3600


class EncryptionConfigResponse(BaseModel):
    id: int
    tenant_id: int
    algorithm: EncryptionAlgorithm
    key_rotation_days: int
    encryption_at_rest: bool
    end_to_end_encryption: bool
    secure_key_delivery: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EncryptionKeyCreate(BaseModel):
    content_id: int
    content_type: str = "movie"
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM


class EncryptionKeyResponse(BaseModel):
    id: int
    key_id: str
    content_id: int
    content_type: str
    algorithm: EncryptionAlgorithm
    status: KeyStatus
    version: int
    created_at: datetime

    class Config:
        from_attributes = True


class KeyDeliveryRequest(BaseModel):
    content_id: int
    content_type: str = "movie"
    session_id: str
    device_id: str


class KeyDeliveryResponse(BaseModel):
    delivery_token: str
    key_id: str
    algorithm: EncryptionAlgorithm
    expires_at: datetime


class EncryptionStatusResponse(BaseModel):
    content_id: int
    content_type: str
    is_encrypted: bool
    algorithm: Optional[EncryptionAlgorithm]
    key_status: Optional[KeyStatus]
    last_rotated: Optional[datetime]
