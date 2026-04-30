"""Content encryption models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class EncryptionAlgorithm(enum.Enum):
    AES_256_GCM = "aes_256_gcm"
    AES_256_CBC = "aes_256_cbc"


class KeyStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    COMPROMISED = "compromised"


class EncryptionConfig(Base):
    """Encryption configuration."""
    __tablename__ = "encryption_configs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    algorithm: Mapped[EncryptionAlgorithm] = mapped_column(SQLEnum(EncryptionAlgorithm), default=EncryptionAlgorithm.AES_256_GCM)
    
    key_rotation_days: Mapped[int] = mapped_column(Integer, default=30)
    
    encryption_at_rest: Mapped[bool] = mapped_column(Boolean, default=True)
    end_to_end_encryption: Mapped[bool] = mapped_column(Boolean, default=False)
    
    secure_key_delivery: Mapped[bool] = mapped_column(Boolean, default=True)
    key_delivery_ttl_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EncryptionKey(Base):
    """Encryption key management."""
    __tablename__ = "encryption_keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")
    
    key_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    encrypted_key: Mapped[str] = mapped_column(String(500), nullable=False)
    
    algorithm: Mapped[EncryptionAlgorithm] = mapped_column(SQLEnum(EncryptionAlgorithm), nullable=False)
    
    status: Mapped[KeyStatus] = mapped_column(SQLEnum(KeyStatus), default=KeyStatus.ACTIVE)
    
    iv: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    version: Mapped[int] = mapped_column(Integer, default=1)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rotated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class KeyDeliveryLog(Base):
    """Key delivery tracking."""
    __tablename__ = "key_delivery_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    key_id: Mapped[int] = mapped_column(Integer, ForeignKey("encryption_keys.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    session_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    delivery_token: Mapped[str] = mapped_column(String(200), nullable=False)
    
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    device_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    delivered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    was_used: Mapped[bool] = mapped_column(Boolean, default=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class SecureKeyStorage(Base):
    """Key storage metadata."""
    __tablename__ = "secure_key_storages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    key_id: Mapped[int] = mapped_column(Integer, ForeignKey("encryption_keys.id"), nullable=False)
    
    storage_type: Mapped[str] = mapped_column(String(50), default="database")
    storage_location: Mapped[str] = mapped_column(String(200), nullable=False)
    
    is_hsm: Mapped[bool] = mapped_column(Boolean, default=False)
    hsm_key_reference: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
