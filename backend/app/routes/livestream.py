from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
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
from datetime import datetime
from typing import List

class ScheduleCreate(BaseModel):
    title: str
    scheduled_start: datetime
    description: Optional[str] = None
    scheduled_end: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None

class DVRSegmentCreate(BaseModel):
    segment_url: str
    start_time: datetime
    end_time: datetime
    segment_duration: int = 10

class NotificationSubscribe(BaseModel):
    notification_type: str = "start"
    notify_before_minutes: int = 5

@router.post("/schedule")
async def schedule_stream(
    data: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Schedule a live stream."""
    service = LiveStreamService(db)
    schedule = await service.schedule_stream(
        streamer_id=current_user.id,
        tenant_id=tenant_id,
        title=data.title,
        scheduled_start=data.scheduled_start,
        description=data.description,
        scheduled_end=data.scheduled_end,
        is_recurring=data.is_recurring,
        recurrence_pattern=data.recurrence_pattern,
    )
    return {
        "id": schedule.id,
        "title": schedule.title,
        "scheduled_start": schedule.scheduled_start.isoformat(),
    }

@router.get("/upcoming")
async def get_upcoming_streams(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get upcoming scheduled streams."""
    service = LiveStreamService(db)
    schedules = await service.get_upcoming_streams(tenant_id, limit)
    return {
        "schedules": [
            {
                "id": s.id,
                "title": s.title,
                "description": s.description,
                "scheduled_start": s.scheduled_start.isoformat(),
                "scheduled_end": s.scheduled_end.isoformat() if s.scheduled_end else None,
                "streamer_id": s.streamer_id,
            }
            for s in schedules
        ]
    }

@router.get("/streams/{stream_id}/dvr")
async def get_dvr_segments(stream_id: int, db: AsyncSession = Depends(get_db)):
    """Get DVR segments for a stream."""
    service = LiveStreamService(db)
    segments = await service.get_dvr_segments(stream_id)
    return {
        "segments": [
            {
                "id": s.id,
                "segment_url": s.segment_url,
                "segment_duration": s.segment_duration,
                "start_time": s.start_time.isoformat(),
                "end_time": s.end_time.isoformat(),
            }
            for s in segments
        ]
    }

@router.post("/streams/{stream_id}/dvr")
async def create_dvr_segment(
    stream_id: int,
    data: DVRSegmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a DVR segment for a stream."""
    service = LiveStreamService(db)
    segment = await service.create_dvr_segment(
        stream_id=stream_id,
        segment_url=data.segment_url,
        start_time=data.start_time,
        end_time=data.end_time,
        segment_duration=data.segment_duration,
    )
    return {"id": segment.id, "segment_url": segment.segment_url}

@router.post("/streams/{stream_id}/subscribe")
async def subscribe_to_stream(
    stream_id: int,
    data: NotificationSubscribe,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Subscribe to stream notifications."""
    service = LiveStreamService(db)
    notification = await service.subscribe_to_stream(
        stream_id=stream_id,
        user_id=current_user.id,
        notification_type=data.notification_type,
        notify_before_minutes=data.notify_before_minutes,
    )
    return {"id": notification.id, "notification_type": notification.notification_type}

@router.put("/streams/{stream_id}/viewers")
async def update_viewer_count(
    stream_id: int,
    viewer_count: int,
    db: AsyncSession = Depends(get_db),
):
    """Update viewer count for a stream."""
    service = LiveStreamService(db)
    stream = await service.update_viewer_count(stream_id, viewer_count)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {"viewer_count": stream.viewer_count, "peak_viewers": stream.peak_viewers}
