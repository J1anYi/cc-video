"""Content encryption service."""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
import hashlib
import base64

from app.models.encryption import (
    EncryptionConfig, EncryptionKey, KeyDeliveryLog, SecureKeyStorage,
    EncryptionAlgorithm, KeyStatus
)


class EncryptionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def configure_encryption(self, tenant_id, algorithm=EncryptionAlgorithm.AES_256_GCM, key_rotation_days=30, encryption_at_rest=True, end_to_end_encryption=False, secure_key_delivery=True, key_delivery_ttl_seconds=3600):
        existing = await self.db.execute(select(EncryptionConfig).where(EncryptionConfig.tenant_id == tenant_id))
        config = existing.scalar_one_or_none()
        if config:
            config.algorithm = algorithm
            config.key_rotation_days = key_rotation_days
            config.encryption_at_rest = encryption_at_rest
            config.end_to_end_encryption = end_to_end_encryption
            config.secure_key_delivery = secure_key_delivery
            config.key_delivery_ttl_seconds = key_delivery_ttl_seconds
            config.updated_at = datetime.utcnow()
        else:
            config = EncryptionConfig(tenant_id=tenant_id, algorithm=algorithm, key_rotation_days=key_rotation_days, encryption_at_rest=encryption_at_rest, end_to_end_encryption=end_to_end_encryption, secure_key_delivery=secure_key_delivery, key_delivery_ttl_seconds=key_delivery_ttl_seconds)
            self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def get_configuration(self, tenant_id):
        result = await self.db.execute(select(EncryptionConfig).where(EncryptionConfig.tenant_id == tenant_id))
        return result.scalar_one_or_none()

    def _generate_key_id(self):
        return secrets.token_hex(16)

    def _generate_encryption_key(self):
        return secrets.token_hex(32)

    def _generate_iv(self):
        return secrets.token_hex(12)

    async def generate_key(self, tenant_id, content_id, content_type="movie", algorithm=EncryptionAlgorithm.AES_256_GCM, key_rotation_days=30):
        key_id = self._generate_key_id()
        raw_key = self._generate_encryption_key()
        encrypted_key = base64.b64encode(hashlib.sha256(raw_key.encode()).digest()).decode()
        iv = self._generate_iv()
        tag = secrets.token_hex(16) if algorithm == EncryptionAlgorithm.AES_256_GCM else None
        key = EncryptionKey(tenant_id=tenant_id, content_id=content_id, content_type=content_type, key_id=key_id, encrypted_key=encrypted_key, algorithm=algorithm, iv=iv, tag=tag, expires_at=datetime.utcnow() + timedelta(days=key_rotation_days))
        self.db.add(key)
        await self.db.commit()
        await self.db.refresh(key)
        storage = SecureKeyStorage(tenant_id=tenant_id, key_id=key.id, storage_type="database", storage_location=f"encryption_keys:{key.id}")
        self.db.add(storage)
        await self.db.commit()
        return key

    async def get_key(self, tenant_id, content_id, content_type="movie"):
        result = await self.db.execute(select(EncryptionKey).where(EncryptionKey.tenant_id == tenant_id, EncryptionKey.content_id == content_id, EncryptionKey.content_type == content_type, EncryptionKey.status == KeyStatus.ACTIVE).order_by(EncryptionKey.created_at.desc()))
        return result.scalar_one_or_none()

    async def deliver_key(self, tenant_id, user_id, content_id, content_type, session_id, device_id, ip_address=None, ttl_seconds=3600):
        key = await self.get_key(tenant_id, content_id, content_type)
        if not key:
            key = await self.generate_key(tenant_id, content_id, content_type)
        delivery_token = secrets.token_urlsafe(32)
        log = KeyDeliveryLog(tenant_id=tenant_id, key_id=key.id, user_id=user_id, session_id=session_id, delivery_token=delivery_token, ip_address=ip_address, device_id=device_id, expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds))
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return key, delivery_token, log.expires_at

    async def get_encryption_status(self, tenant_id, content_id, content_type="movie"):
        key = await self.get_key(tenant_id, content_id, content_type)
        if not key:
            return False, None, None, None
        return True, key.algorithm, key.status, key.rotated_at

    async def rotate_key(self, tenant_id, content_id, content_type="movie"):
        old_key = await self.get_key(tenant_id, content_id, content_type)
        if old_key:
            old_key.status = KeyStatus.EXPIRED
            old_key.rotated_at = datetime.utcnow()
            await self.db.commit()
        config = await self.get_configuration(tenant_id)
        new_key = await self.generate_key(tenant_id, content_id, content_type, algorithm=config.algorithm if config else EncryptionAlgorithm.AES_256_GCM, key_rotation_days=config.key_rotation_days if config else 30)
        return old_key, new_key
