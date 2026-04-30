import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.password_reset import PasswordReset
from app.models.user import User
from app.services.auth import auth_service


class PasswordResetService:
    def __init__(self):
        self.token_expire_hours = 1

    def _hash_token(self, token: str) -> str:
        """Hash a token using SHA-256."""
        return hashlib.sha256(token.encode()).hexdigest()

    async def create_reset_token(self, db: AsyncSession, user_id: int) -> str:
        """
        Generate a password reset token for a user.
        Returns the plaintext token (sent to user) while storing the hash.
        """
        # Generate secure random token
        plaintext_token = secrets.token_urlsafe(32)
        token_hash = self._hash_token(plaintext_token)

        # Set expiration
        expires_at = datetime.now(timezone.utc) + timedelta(hours=self.token_expire_hours)

        # Create reset record
        reset = PasswordReset(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(reset)
        await db.commit()

        return plaintext_token

    async def validate_token(self, db: AsyncSession, token: str) -> User | None:
        """
        Validate a password reset token.
        Returns the associated user if valid, None otherwise.
        """
        token_hash = self._hash_token(token)
        now = datetime.now(timezone.utc)

        # Find valid token
        stmt = select(PasswordReset).where(
            and_(
                PasswordReset.token_hash == token_hash,
                PasswordReset.expires_at > now,
                PasswordReset.used_at.is_(None),
            )
        )
        result = await db.execute(stmt)
        reset = result.scalar_one_or_none()

        if not reset:
            return None

        # Get associated user
        stmt = select(User).where(User.id == reset.user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def reset_password(self, db: AsyncSession, token: str, new_password: str) -> bool:
        """
        Reset a user's password using a valid token.
        Marks the token as used after successful reset.
        """
        token_hash = self._hash_token(token)
        now = datetime.now(timezone.utc)

        # Find valid token
        stmt = select(PasswordReset).where(
            and_(
                PasswordReset.token_hash == token_hash,
                PasswordReset.expires_at > now,
                PasswordReset.used_at.is_(None),
            )
        )
        result = await db.execute(stmt)
        reset = result.scalar_one_or_none()

        if not reset:
            return False

        # Get user
        stmt = select(User).where(User.id == reset.user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return False

        # Update password
        user.hashed_password = auth_service.get_password_hash(new_password)
        user.updated_at = datetime.utcnow()

        # Mark token as used
        reset.used_at = now

        await db.commit()
        return True

    async def cleanup_expired_tokens(self, db: AsyncSession) -> int:
        """
        Remove expired password reset tokens.
        Returns the number of tokens removed.
        """
        now = datetime.now(timezone.utc)
        stmt = select(PasswordReset).where(PasswordReset.expires_at < now)
        result = await db.execute(stmt)
        expired = result.scalars().all()

        for token in expired:
            await db.delete(token)

        await db.commit()
        return len(expired)


password_reset_service = PasswordResetService()
