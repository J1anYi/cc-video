"""Watch Party routes for synchronized viewing events."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.watch_party_service import WatchPartyService


router = APIRouter(prefix="/watch-parties", tags=["watch-parties"])
service = WatchPartyService()


class PartyCreate(BaseModel):
    title: str
    movie_id: int
    scheduled_start: str
    description: Optional[str] = None
    is_public: bool = True
    max_participants: Optional[int] = None


class ChatMessage(BaseModel):
    message: str
    playback_time: float = 0


class InvitationCreate(BaseModel):
    user_id: int


@router.post("")
async def create_party(data: PartyCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    scheduled = datetime.fromisoformat(data.scheduled_start.replace("Z", "+00:00"))
    party = await service.create_party(db, current_user.tenant_id, data.movie_id, current_user.id, data.title, scheduled, data.description, data.is_public, data.max_participants)
    return {"id": party.id, "title": party.title}


@router.get("")
async def get_upcoming_parties(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    parties = await service.get_upcoming_parties(db, current_user.tenant_id)
    return [{"id": p.id, "title": p.title, "movie_id": p.movie_id, "scheduled_start": p.scheduled_start.isoformat()} for p in parties]


@router.get("/my")
async def get_my_parties(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    parties = await service.get_user_parties(db, current_user.id)
    return [{"id": p.id, "title": p.title, "status": p.status.value} for p in parties]


@router.get("/{party_id}")
async def get_party(party_id: int, db: AsyncSession = Depends(get_db)):
    party = await service.get_party(db, party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return {"id": party.id, "title": party.title, "movie_id": party.movie_id, "status": party.status.value}


@router.post("/{party_id}/join")
async def join_party(party_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    participant = await service.join_party(db, party_id, current_user.id, current_user.tenant_id)
    if not participant:
        raise HTTPException(status_code=400, detail="Cannot join party")
    return {"message": "Joined party"}


@router.post("/{party_id}/leave")
async def leave_party(party_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not await service.leave_party(db, party_id, current_user.id):
        raise HTTPException(status_code=400, detail="Cannot leave party")
    return {"message": "Left party"}


@router.get("/{party_id}/participants")
async def get_participants(party_id: int, db: AsyncSession = Depends(get_db)):
    participants = await service.get_participants(db, party_id)
    return [{"user_id": p.user_id, "role": p.role.value} for p in participants]


@router.post("/{party_id}/invite")
async def invite_user(party_id: int, data: InvitationCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    invitation = await service.invite_user(db, party_id, data.user_id, current_user.id, current_user.tenant_id)
    if not invitation:
        raise HTTPException(status_code=400, detail="Cannot invite")
    return {"id": invitation.id}


@router.post("/{party_id}/chat")
async def send_chat(party_id: int, data: ChatMessage, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = await service.send_chat_message(db, party_id, current_user.id, current_user.tenant_id, data.message, data.playback_time)
    return {"id": chat.id, "message": chat.message}


@router.get("/{party_id}/chat")
async def get_chat(party_id: int, db: AsyncSession = Depends(get_db)):
    messages = await service.get_chat_messages(db, party_id)
    return [{"id": m.id, "user_id": m.user_id, "message": m.message} for m in messages]
