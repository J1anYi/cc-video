from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, Boolean, Index, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
import enum

from app.database import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.password_reset import PasswordReset
    from app.models.video_chapter import UserBookmark
    from app.models.creator import CreatorProfile


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    PLATFORM_ADMIN = "platform_admin"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index('ix_users_created_at', 'created_at'),
        Index('ix_users_tenant_id', 'tenant_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_suspended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    warnings_count: Mapped[int] = mapped_column(default=0, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Tenant association
    tenant_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=True)
    tenant: Mapped[Optional["Tenant"]] = relationship("Tenant", back_populates="users")

    # i18n preferences
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)

    # Relationships
    password_resets: Mapped[list["PasswordReset"]] = relationship("PasswordReset", back_populates="user")
    bookmarks: Mapped[list["UserBookmark"]] = relationship("UserBookmark", back_populates="user")
    creator_profile: Mapped[Optional["CreatorProfile"]] = relationship("CreatorProfile", back_populates="user", uselist=False)

    # Personalization preferences
    homepage_layout: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    genre_weights: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    mood_preferences: Mapped[str | None] = mapped_column(String(500), nullable=True)
    email_digest_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_digest_frequency: Mapped[str] = mapped_column(String(20), default="weekly", nullable=False)

    # Profile customization
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    banner_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(500), nullable=True)
    profile_theme: Mapped[str] = mapped_column(String(50), default="default", nullable=False)
    
    # Premium features
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    premium_since: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    badges: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Subscription fields
    subscription_tier: Mapped[str] = mapped_column(String(20), default="free", nullable=False)
    subscription_status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    subscription_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    subscription_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    @property
    def is_admin(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.PLATFORM_ADMIN)

    @property
    def is_platform_admin(self) -> bool:
        return self.role == UserRole.PLATFORM_ADMIN
