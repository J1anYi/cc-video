"""Watch Party models for synchronized viewing events."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class WatchPartyStatus(enum.Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    ENDED = "ended"
    CANCELLED = "cancelled"


class WatchPartyRole(enum.Enum):
    HOST = "host"
    CO_HOST = "co_host"
    PARTICIPANT = "participant"


class WatchParty(Base):
    """Scheduled watch party event."""
    __tablename__ = "watch_parties"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    host_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    scheduled_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    actual_start: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    status: Mapped[WatchPartyStatus] = mapped_column(SQLEnum(WatchPartyStatus), default=WatchPartyStatus.SCHEDULED)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    participant_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class WatchPartyParticipant(Base):
    """Participant in a watch party."""
    __tablename__ = "watch_party_participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    party_id: Mapped[int] = mapped_column(Integer, ForeignKey("watch_parties.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    role: Mapped[WatchPartyRole] = mapped_column(SQLEnum(WatchPartyRole), default=WatchPartyRole.PARTICIPANT)
    playback_position: Mapped[float] = mapped_column(default=0.0)
    is_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    
    joined_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class WatchPartyInvitation(Base):
    """Invitation to a watch party."""
    __tablename__ = "watch_party_invitations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    party_id: Mapped[int] = mapped_column(Integer, ForeignKey("watch_parties.id"), nullable=False, index=True)
    invited_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    invited_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class WatchPartyChat(Base):
    """Chat message during watch party."""
    __tablename__ = "watch_party_chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    party_id: Mapped[int] = mapped_column(Integer, ForeignKey("watch_parties.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    message: Mapped[str] = mapped_column(Text, nullable=False)
    playback_time: Mapped[float] = mapped_column(default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class WatchPartyReminder(Base):
    """Reminder for a watch party."""
    __tablename__ = "watch_party_reminders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    party_id: Mapped[int] = mapped_column(Integer, ForeignKey("watch_parties.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    reminder_minutes: Mapped[int] = mapped_column(Integer, default=15)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
