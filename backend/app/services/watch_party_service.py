"""Watch Party service for synchronized viewing events."""
import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.watch_party import (
    WatchParty, WatchPartyParticipant, WatchPartyInvitation,
    WatchPartyChat, WatchPartyReminder,
    WatchPartyStatus, WatchPartyRole
)


class WatchPartyService:
    """Service for watch party operations."""
    
    async def create_party(
        self, session: AsyncSession, tenant_id: int, movie_id: int, host_id: int,
        title: str, scheduled_start: datetime, description: Optional[str] = None,
        is_public: bool = True, max_participants: Optional[int] = None
    ) -> WatchParty:
        party = WatchParty(
            tenant_id=tenant_id, movie_id=movie_id, host_id=host_id,
            title=title, description=description, scheduled_start=scheduled_start,
            is_public=is_public, max_participants=max_participants
        )
        session.add(party)
        await session.flush()
        participant = WatchPartyParticipant(
            party_id=party.id, user_id=host_id, tenant_id=tenant_id, role=WatchPartyRole.HOST
        )
        session.add(participant)
        party.participant_count = 1
        await session.commit()
        return party
    
    async def get_party(self, session: AsyncSession, party_id: int) -> Optional[WatchParty]:
        result = await session.execute(select(WatchParty).where(WatchParty.id == party_id))
        return result.scalar_one_or_none()
    
    async def get_upcoming_parties(self, session: AsyncSession, tenant_id: int) -> List[WatchParty]:
        result = await session.execute(
            select(WatchParty).where(
                WatchParty.tenant_id == tenant_id,
                WatchParty.status == WatchPartyStatus.SCHEDULED,
                WatchParty.scheduled_start > datetime.utcnow()
            ).order_by(WatchParty.scheduled_start)
        )
        return list(result.scalars().all())
    
    async def get_user_parties(self, session: AsyncSession, user_id: int) -> List[WatchParty]:
        participant_parties = select(WatchPartyParticipant.party_id).where(
            WatchPartyParticipant.user_id == user_id
        )
        result = await session.execute(
            select(WatchParty).where(WatchParty.id.in_(participant_parties))
            .order_by(WatchParty.scheduled_start.desc())
        )
        return list(result.scalars().all())
    
    async def update_party(self, session: AsyncSession, party_id: int, **kwargs) -> Optional[WatchParty]:
        party = await self.get_party(session, party_id)
        if not party:
            return None
        for key, value in kwargs.items():
            if hasattr(party, key) and value is not None:
                setattr(party, key, value)
        party.updated_at = datetime.utcnow()
        await session.commit()
        return party
    
    async def cancel_party(self, session: AsyncSession, party_id: int) -> bool:
        party = await self.get_party(session, party_id)
        if not party:
            return False
        party.status = WatchPartyStatus.CANCELLED
        await session.commit()
        return True
    
    async def start_party(self, session: AsyncSession, party_id: int) -> Optional[WatchParty]:
        party = await self.get_party(session, party_id)
        if not party:
            return None
        party.status = WatchPartyStatus.LIVE
        party.actual_start = datetime.utcnow()
        await session.commit()
        return party
    
    async def end_party(self, session: AsyncSession, party_id: int) -> Optional[WatchParty]:
        party = await self.get_party(session, party_id)
        if not party:
            return None
        party.status = WatchPartyStatus.ENDED
        party.actual_end = datetime.utcnow()
        await session.commit()
        return party

    async def join_party(self, session: AsyncSession, party_id: int, user_id: int, tenant_id: int) -> Optional[WatchPartyParticipant]:
        party = await self.get_party(session, party_id)
        if not party or party.status not in [WatchPartyStatus.SCHEDULED, WatchPartyStatus.LIVE]:
            return None
        if party.max_participants and party.participant_count >= party.max_participants:
            return None
        existing = await session.execute(
            select(WatchPartyParticipant).where(
                WatchPartyParticipant.party_id == party_id,
                WatchPartyParticipant.user_id == user_id
            )
        )
        if existing.scalar_one_or_none():
            return None
        participant = WatchPartyParticipant(party_id=party_id, user_id=user_id, tenant_id=tenant_id)
        session.add(participant)
        party.participant_count += 1
        await session.commit()
        return participant
    
    async def leave_party(self, session: AsyncSession, party_id: int, user_id: int) -> bool:
        result = await session.execute(
            select(WatchPartyParticipant).where(
                WatchPartyParticipant.party_id == party_id,
                WatchPartyParticipant.user_id == user_id
            )
        )
        participant = result.scalar_one_or_none()
        if not participant or participant.role == WatchPartyRole.HOST:
            return False
        await session.delete(participant)
        party = await self.get_party(session, party_id)
        if party:
            party.participant_count = max(0, party.participant_count - 1)
        await session.commit()
        return True
    
    async def get_participants(self, session: AsyncSession, party_id: int) -> List[WatchPartyParticipant]:
        result = await session.execute(
            select(WatchPartyParticipant).where(WatchPartyParticipant.party_id == party_id)
            .order_by(WatchPartyParticipant.joined_at)
        )
        return list(result.scalars().all())
    
    async def update_playback_position(self, session: AsyncSession, party_id: int, user_id: int, position: float) -> bool:
        result = await session.execute(
            select(WatchPartyParticipant).where(
                WatchPartyParticipant.party_id == party_id,
                WatchPartyParticipant.user_id == user_id
            )
        )
        participant = result.scalar_one_or_none()
        if not participant:
            return False
        participant.playback_position = position
        await session.commit()
        return True
    
    async def invite_user(self, session: AsyncSession, party_id: int, user_id: int, invited_by: int, tenant_id: int) -> Optional[WatchPartyInvitation]:
        party = await self.get_party(session, party_id)
        if not party:
            return None
        existing = await session.execute(
            select(WatchPartyInvitation).where(
                WatchPartyInvitation.party_id == party_id,
                WatchPartyInvitation.invited_user_id == user_id
            )
        )
        if existing.scalar_one_or_none():
            return None
        invitation = WatchPartyInvitation(
            party_id=party_id, invited_user_id=user_id,
            invited_by=invited_by, tenant_id=tenant_id
        )
        session.add(invitation)
        await session.commit()
        return invitation
    
    async def accept_invitation(self, session: AsyncSession, invitation_id: int) -> Optional[WatchPartyParticipant]:
        result = await session.execute(
            select(WatchPartyInvitation).where(WatchPartyInvitation.id == invitation_id)
        )
        invitation = result.scalar_one_or_none()
        if not invitation or invitation.is_accepted:
            return None
        participant = await self.join_party(
            session, invitation.party_id, invitation.invited_user_id, invitation.tenant_id
        )
        if participant:
            invitation.is_accepted = True
            invitation.accepted_at = datetime.utcnow()
            await session.commit()
        return participant
    
    async def send_chat_message(self, session: AsyncSession, party_id: int, user_id: int, tenant_id: int, message: str, playback_time: float = 0) -> WatchPartyChat:
        chat = WatchPartyChat(
            party_id=party_id, user_id=user_id, tenant_id=tenant_id,
            message=message, playback_time=playback_time
        )
        session.add(chat)
        await session.commit()
        return chat
    
    async def get_chat_messages(self, session: AsyncSession, party_id: int, limit: int = 100) -> List[WatchPartyChat]:
        result = await session.execute(
            select(WatchPartyChat).where(WatchPartyChat.party_id == party_id)
            .order_by(WatchPartyChat.created_at).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create_reminder(self, session: AsyncSession, party_id: int, user_id: int, tenant_id: int, reminder_minutes: int = 15) -> WatchPartyReminder:
        reminder = WatchPartyReminder(
            party_id=party_id, user_id=user_id, tenant_id=tenant_id,
            reminder_minutes=reminder_minutes
        )
        session.add(reminder)
        await session.commit()
        return reminder
    
    async def get_reminders(self, session: AsyncSession, party_id: int) -> List[WatchPartyReminder]:
        result = await session.execute(
            select(WatchPartyReminder).where(WatchPartyReminder.party_id == party_id)
        )
        return list(result.scalars().all())
    
    async def is_host(self, session: AsyncSession, party_id: int, user_id: int) -> bool:
        result = await session.execute(
            select(WatchPartyParticipant).where(
                WatchPartyParticipant.party_id == party_id,
                WatchPartyParticipant.user_id == user_id,
                WatchPartyParticipant.role == WatchPartyRole.HOST
            )
        )
        return result.scalar_one_or_none() is not None
