"""Access control service."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets

from app.models.access import (
    AccessPolicy, ContentPermission, TimeWindow, DeviceLimit, StreamSession,
    AccessLevel, TimeWindowType, PermissionType
)


class AccessControlService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_policy(self, tenant_id, name, description=None, default_level=AccessLevel.FULL, max_devices=5, max_concurrent_streams=2):
        policy = AccessPolicy(tenant_id=tenant_id, name=name, description=description, default_level=default_level, max_devices=max_devices, max_concurrent_streams=max_concurrent_streams)
        self.db.add(policy)
        await self.db.commit()
        await self.db.refresh(policy)
        return policy

    async def list_policies(self, tenant_id):
        result = await self.db.execute(select(AccessPolicy).where(AccessPolicy.tenant_id == tenant_id, AccessPolicy.is_active == True))
        return result.scalars().all()

    async def set_permission(self, tenant_id, content_id, content_type, granted_by, user_id=None, role_id=None, permission_type=PermissionType.VIEW, access_level=AccessLevel.FULL, expires_at=None):
        perm = ContentPermission(tenant_id=tenant_id, content_id=content_id, content_type=content_type, user_id=user_id, role_id=role_id, permission_type=permission_type, access_level=access_level, granted_by=granted_by, expires_at=expires_at)
        self.db.add(perm)
        await self.db.commit()
        await self.db.refresh(perm)
        return perm

    async def check_access(self, tenant_id, user_id, content_id, content_type, device_id, permission_type=PermissionType.VIEW, ip_address=None):
        result = await self.db.execute(select(AccessPolicy).where(AccessPolicy.tenant_id == tenant_id, AccessPolicy.is_active == True))
        policy = result.scalar_one_or_none()
        if not policy:
            return True, AccessLevel.FULL, None, None
        perm_result = await self.db.execute(select(ContentPermission).where(ContentPermission.tenant_id == tenant_id, ContentPermission.content_id == content_id, ContentPermission.user_id == user_id, ContentPermission.permission_type == permission_type))
        permission = perm_result.scalar_one_or_none()
        access_level = permission.access_level if permission else policy.default_level
        if access_level == AccessLevel.NONE:
            return False, access_level, "Access denied", None
        stream_result = await self.db.execute(select(StreamSession).where(StreamSession.user_id == user_id, StreamSession.is_active == True))
        active_streams = stream_result.scalars().all()
        if len(active_streams) >= policy.max_concurrent_streams:
            return False, access_level, "Concurrent stream limit reached", None
        session_token = secrets.token_urlsafe(32)
        session = StreamSession(tenant_id=tenant_id, user_id=user_id, content_id=content_id, content_type=content_type, device_id=device_id, session_token=session_token, ip_address=ip_address)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return True, access_level, None, session_token

    async def list_sessions(self, tenant_id, user_id):
        result = await self.db.execute(select(StreamSession).where(StreamSession.tenant_id == tenant_id, StreamSession.user_id == user_id, StreamSession.is_active == True))
        return result.scalars().all()

    async def terminate_session(self, tenant_id, user_id, session_id):
        result = await self.db.execute(select(StreamSession).where(StreamSession.id == session_id, StreamSession.tenant_id == tenant_id, StreamSession.user_id == user_id))
        session = result.scalar_one_or_none()
        if session:
            session.is_active = False
            session.ended_at = datetime.utcnow()
            await self.db.commit()
            return True
        return False

    async def set_device_limit(self, tenant_id, user_id, max_devices=5, max_streams=2):
        result = await self.db.execute(select(DeviceLimit).where(DeviceLimit.tenant_id == tenant_id, DeviceLimit.user_id == user_id))
        limit = result.scalar_one_or_none()
        if limit:
            limit.max_devices = max_devices
            limit.max_streams = max_streams
            limit.updated_at = datetime.utcnow()
        else:
            limit = DeviceLimit(tenant_id=tenant_id, user_id=user_id, max_devices=max_devices, max_streams=max_streams)
            self.db.add(limit)
        await self.db.commit()
        await self.db.refresh(limit)
        return limit
