"""DRM service for content protection."""
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
import hashlib
import base64

from app.models.drm import (
    DRMConfiguration, DRMKey, DeviceRegistration, DRMLicense, OfflineDRMToken,
    DRMProvider, DRMKeyStatus, DeviceType
)


class DRMService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def configure_drm(self, tenant_id, provider, widevine_license_url=None, widevine_provider_id=None, playready_license_url=None, playready_key_id=None, fairplay_license_url=None, fairplay_cert_url=None, max_devices_per_user=5, offline_playback_enabled=False, offline_duration_hours=168, key_rotation_days=30):
        existing = await self.db.execute(select(DRMConfiguration).where(DRMConfiguration.tenant_id == tenant_id, DRMConfiguration.is_active == True))
        config = existing.scalar_one_or_none()
        if config:
            config.provider = provider
            config.widevine_license_url = widevine_license_url
            config.widevine_provider_id = widevine_provider_id
            config.playready_license_url = playready_license_url
            config.playready_key_id = playready_key_id
            config.fairplay_license_url = fairplay_license_url
            config.fairplay_cert_url = fairplay_cert_url
            config.max_devices_per_user = max_devices_per_user
            config.offline_playback_enabled = offline_playback_enabled
            config.offline_duration_hours = offline_duration_hours
            config.key_rotation_days = key_rotation_days
            config.updated_at = datetime.utcnow()
        else:
            config = DRMConfiguration(tenant_id=tenant_id, provider=provider, widevine_license_url=widevine_license_url, widevine_provider_id=widevine_provider_id, playready_license_url=playready_license_url, playready_key_id=playready_key_id, fairplay_license_url=fairplay_license_url, fairplay_cert_url=fairplay_cert_url, max_devices_per_user=max_devices_per_user, offline_playback_enabled=offline_playback_enabled, offline_duration_hours=offline_duration_hours, key_rotation_days=key_rotation_days)
            self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def get_configuration(self, tenant_id):
        result = await self.db.execute(select(DRMConfiguration).where(DRMConfiguration.tenant_id == tenant_id, DRMConfiguration.is_active == True))
        return result.scalar_one_or_none()

    def _generate_key_id(self):
        return secrets.token_hex(16)

    def _generate_encryption_key(self):
        return secrets.token_hex(32)

    def _generate_iv(self):
        return secrets.token_hex(8)

    async def generate_content_key(self, tenant_id, content_id, content_type, provider, expires_days=30):
        key = DRMKey(tenant_id=tenant_id, content_id=content_id, content_type=content_type, key_id=self._generate_key_id(), encryption_key=self._generate_encryption_key(), provider=provider, status=DRMKeyStatus.ACTIVE, iv=self._generate_iv(), expires_at=datetime.utcnow() + timedelta(days=expires_days))
        self.db.add(key)
        await self.db.commit()
        await self.db.refresh(key)
        return key

    async def get_content_key(self, tenant_id, content_id, content_type):
        result = await self.db.execute(select(DRMKey).where(DRMKey.tenant_id == tenant_id, DRMKey.content_id == content_id, DRMKey.content_type == content_type, DRMKey.status == DRMKeyStatus.ACTIVE).order_by(DRMKey.created_at.desc()))
        return result.scalar_one_or_none()

    async def issue_license(self, tenant_id, user_id, content_id, content_type, device_id, provider, duration_hours=24):
        key = await self.get_content_key(tenant_id, content_id, content_type)
        if not key:
            key = await self.generate_content_key(tenant_id, content_id, content_type, provider)
        device_result = await self.db.execute(select(DeviceRegistration).where(DeviceRegistration.device_id == device_id, DeviceRegistration.user_id == user_id))
        device = device_result.scalar_one_or_none()
        license_token = secrets.token_urlsafe(32)
        license = DRMLicense(tenant_id=tenant_id, user_id=user_id, key_id=key.id, device_id=device.id if device else None, license_token=license_token, content_id=content_id, content_type=content_type, provider=provider, expires_at=datetime.utcnow() + timedelta(hours=duration_hours))
        self.db.add(license)
        await self.db.commit()
        await self.db.refresh(license)
        return license, key

    async def register_device(self, tenant_id, user_id, device_id, device_name, device_type, drm_provider, user_agent=None, ip_address=None, max_devices=5):
        existing = await self.db.execute(select(DeviceRegistration).where(DeviceRegistration.device_id == device_id, DeviceRegistration.user_id == user_id))
        device = existing.scalar_one_or_none()
        if device:
            device.last_used_at = datetime.utcnow()
            device.is_active = True
            await self.db.commit()
            await self.db.refresh(device)
            return device
        count_result = await self.db.execute(select(DeviceRegistration).where(DeviceRegistration.user_id == user_id, DeviceRegistration.is_active == True))
        active_devices = count_result.scalars().all()
        if len(active_devices) >= max_devices:
            oldest = min(active_devices, key=lambda d: d.last_used_at or d.created_at)
            oldest.is_active = False
            await self.db.commit()
        device = DeviceRegistration(tenant_id=tenant_id, user_id=user_id, device_id=device_id, device_name=device_name, device_type=device_type, drm_provider=drm_provider, user_agent=user_agent, ip_address=ip_address, last_used_at=datetime.utcnow())
        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)
        return device

    async def list_devices(self, tenant_id, user_id):
        result = await self.db.execute(select(DeviceRegistration).where(DeviceRegistration.tenant_id == tenant_id, DeviceRegistration.user_id == user_id, DeviceRegistration.is_active == True).order_by(DeviceRegistration.last_used_at.desc()))
        return result.scalars().all()

    async def remove_device(self, tenant_id, user_id, device_id):
        result = await self.db.execute(select(DeviceRegistration).where(DeviceRegistration.id == device_id, DeviceRegistration.tenant_id == tenant_id, DeviceRegistration.user_id == user_id))
        device = result.scalar_one_or_none()
        if device:
            device.is_active = False
            await self.db.commit()
            return True
        return False

    async def generate_offline_token(self, tenant_id, user_id, content_id, content_type, device_id, provider, duration_hours=168):
        key = await self.get_content_key(tenant_id, content_id, content_type)
        if not key:
            key = await self.generate_content_key(tenant_id, content_id, content_type, provider)
        device_result = await self.db.execute(select(DeviceRegistration).where(DeviceRegistration.device_id == device_id, DeviceRegistration.user_id == user_id))
        device = device_result.scalar_one_or_none()
        if not device:
            raise ValueError("Device must be registered for offline playback")
        token = secrets.token_urlsafe(32)
        encrypted_key = base64.b64encode(hashlib.sha256(f"{key.encryption_key}:{user_id}:{device_id}".encode()).digest()).decode()
        offline_token = OfflineDRMToken(tenant_id=tenant_id, user_id=user_id, token=token, content_id=content_id, content_type=content_type, device_id=device.id, encrypted_key=encrypted_key, expires_at=datetime.utcnow() + timedelta(hours=duration_hours))
        self.db.add(offline_token)
        await self.db.commit()
        await self.db.refresh(offline_token)
        return offline_token, key

    async def rotate_keys(self, tenant_id, content_id, content_type):
        old_key = await self.get_content_key(tenant_id, content_id, content_type)
        if old_key:
            old_key.status = DRMKeyStatus.EXPIRED
            old_key.rotated_at = datetime.utcnow()
        new_key = await self.generate_content_key(tenant_id, content_id, content_type, old_key.provider if old_key else DRMProvider.WIDEVINE)
        await self.db.commit()
        return old_key, new_key

    async def validate_license(self, license_token):
        result = await self.db.execute(select(DRMLicense).where(DRMLicense.license_token == license_token, DRMLicense.is_valid == True, DRMLicense.expires_at > datetime.utcnow()))
        return result.scalar_one_or_none()
