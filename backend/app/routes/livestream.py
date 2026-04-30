from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.auth import get_current_user
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.services.livestream_service import LiveStreamService

router = APIRouter(prefix="/live", tags=["livestream"])


class StreamCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ChatMessage(BaseModel):
    message: str


class ReactionCreate(BaseModel):
    reaction_type: str


@router.post("/streams")
async def create_stream(data: StreamCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    service = LiveStreamService(db)
    stream = await service.create_stream(title=data.title, streamer_id=current_user.id, tenant_id=tenant_id, description=data.description)
    return {"id": stream.id, "title": stream.title, "status": stream.status.value}


@router.get("/streams")
async def get_streams(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    service = LiveStreamService(db)
    streams = await service.get_active_streams(tenant_id)
    return {"streams": [{"id": s.id, "title": s.title, "status": s.status.value, "viewer_count": s.viewer_count} for s in streams]}


@router.get("/streams/{stream_id}")
async def get_stream(stream_id: int, db: AsyncSession = Depends(get_db)):
    service = LiveStreamService(db)
    stream = await service.get_stream(stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {"id": stream.id, "title": stream.title, "status": stream.status.value, "viewer_count": stream.viewer_count}


@router.post("/streams/{stream_id}/start")
async def start_stream(stream_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LiveStreamService(db)
    stream = await service.start_stream(stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {"id": stream.id, "status": stream.status.value}


@router.post("/streams/{stream_id}/end")
async def end_stream(stream_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LiveStreamService(db)
    stream = await service.end_stream(stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {"id": stream.id, "status": stream.status.value}


@router.post("/streams/{stream_id}/chat")
async def send_chat(stream_id: int, data: ChatMessage, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LiveStreamService(db)
    chat = await service.send_chat(stream_id=stream_id, user_id=current_user.id, message=data.message)
    return {"id": chat.id, "message": chat.message}


@router.post("/streams/{stream_id}/reactions")
async def send_reaction(stream_id: int, data: ReactionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LiveStreamService(db)
    reaction = await service.send_reaction(stream_id=stream_id, user_id=current_user.id, reaction_type=data.reaction_type)
    return {"id": reaction.id, "reaction_type": reaction.reaction_type}
