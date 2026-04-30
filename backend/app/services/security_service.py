from datetime import datetime
from typing import Optional
import secrets
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.security import AuditLog, TwoFactorAuth, DataExportRequest, DataDeletionRequest
from app.models.user import User


class SecurityService:
    """Service for security and compliance operations."""

    async def log_action(
        self,
        db: AsyncSession,
        action: str,
        user_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Log an audit action."""
        log = AuditLog(
            user_id=user_id,
            tenant_id=tenant_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    async def get_audit_logs(
        self,
        db: AsyncSession,
        user_id: Optional[int] = None,
        tenant_id: Optional[int] = None,
        action: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        """Get audit logs with optional filters."""
        query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if tenant_id:
            query = query.where(AuditLog.tenant_id == tenant_id)
        if action:
            query = query.where(AuditLog.action == action)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def enable_2fa(self, db: AsyncSession, user_id: int) -> TwoFactorAuth:
        """Enable 2FA for a user."""
        secret = secrets.token_hex(16)
        backup_codes = [secrets.token_hex(8) for _ in range(10)]
        
        existing = await self.get_2fa(db, user_id)
        if existing:
            existing.secret = secret
            existing.is_enabled = True
            existing.backup_codes = json.dumps(backup_codes)
            await db.commit()
            await db.refresh(existing)
            return existing
        
        tfa = TwoFactorAuth(user_id=user_id, secret=secret, is_enabled=True, backup_codes=json.dumps(backup_codes))
        db.add(tfa)
        await db.commit()
        await db.refresh(tfa)
        return tfa

    async def disable_2fa(self, db: AsyncSession, user_id: int) -> Optional[TwoFactorAuth]:
        """Disable 2FA for a user."""
        tfa = await self.get_2fa(db, user_id)
        if tfa:
            tfa.is_enabled = False
            await db.commit()
            await db.refresh(tfa)
        return tfa

    async def get_2fa(self, db: AsyncSession, user_id: int) -> Optional[TwoFactorAuth]:
        """Get 2FA settings for a user."""
        result = await db.execute(select(TwoFactorAuth).where(TwoFactorAuth.user_id == user_id))
        return result.scalar_one_or_none()

    async def verify_2fa(self, db: AsyncSession, user_id: int, code: str) -> bool:
        """Verify a 2FA code."""
        tfa = await self.get_2fa(db, user_id)
        if not tfa or not tfa.is_enabled:
            return False
        
        # Check backup codes
        if tfa.backup_codes:
            backup_codes = json.loads(tfa.backup_codes)
            if code in backup_codes:
                backup_codes.remove(code)
                tfa.backup_codes = json.dumps(backup_codes)
                tfa.last_used_at = datetime.utcnow()
                await db.commit()
                return True
        
        # Simple verification (in production, use proper TOTP)
        if code == tfa.secret[:6]:
            tfa.last_used_at = datetime.utcnow()
            await db.commit()
            return True
        
        return False

    async def request_data_export(self, db: AsyncSession, user_id: int) -> DataExportRequest:
        """Request a GDPR data export."""
        request = DataExportRequest(user_id=user_id)
        db.add(request)
        await db.commit()
        await db.refresh(request)
        return request

    async def request_data_deletion(self, db: AsyncSession, user_id: int) -> DataDeletionRequest:
        """Request GDPR data deletion."""
        request = DataDeletionRequest(user_id=user_id)
        db.add(request)
        await db.commit()
        await db.refresh(request)
        return request

    async def export_user_data(self, db: AsyncSession, user_id: int) -> dict:
        """Export all user data for GDPR compliance."""
        user = await db.execute(select(User).where(User.id == user_id))
        user_data = user.scalar_one_or_none()
        
        return {
            "user": {
                "id": user_data.id,
                "email": user_data.email,
                "display_name": user_data.display_name,
                "created_at": user_data.created_at.isoformat() if user_data.created_at else None,
            },
            "exported_at": datetime.utcnow().isoformat(),
        }


security_service = SecurityService()
