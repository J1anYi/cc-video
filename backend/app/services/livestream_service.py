from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.livestream import LiveStream, LiveChat, StreamReaction, StreamStatus, LiveStreamSchedule, LiveStreamDVR, LiveStreamNotification


class LiveStreamService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_stream(self, title: str, streamer_id: int, tenant_id: int, description: Optional[str] = None) -> LiveStream:
        stream = LiveStream(title=title, description=description, streamer_id=streamer_id, tenant_id=tenant_id)
        self.db.add(stream)
        await self.db.commit()
        await self.db.refresh(stream)
        return stream

    async def start_stream(self, stream_id: int) -> Optional[LiveStream]:
        stream = await self.db.get(LiveStream, stream_id)
        if stream:
            stream.status = StreamStatus.LIVE
            stream.started_at = datetime.utcnow()
            await self.db.commit()
        return stream

    async def end_stream(self, stream_id: int) -> Optional[LiveStream]:
        stream = await self.db.get(LiveStream, stream_id)
        if stream:
            stream.status = StreamStatus.ENDED
            stream.ended_at = datetime.utcnow()
            await self.db.commit()
        return stream

    async def get_stream(self, stream_id: int) -> Optional[LiveStream]:
        return await self.db.get(LiveStream, stream_id)

    async def get_active_streams(self, tenant_id: int) -> List[LiveStream]:
        query = select(LiveStream).where(LiveStream.tenant_id == tenant_id, LiveStream.status == StreamStatus.LIVE)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def send_chat(self, stream_id: int, user_id: int, message: str) -> LiveChat:
        chat = LiveChat(stream_id=stream_id, user_id=user_id, message=message)
        self.db.add(chat)
        await self.db.commit()
        return chat

    async def send_reaction(self, stream_id: int, user_id: int, reaction_type: str) -> StreamReaction:
        reaction = StreamReaction(stream_id=stream_id, user_id=user_id, reaction_type=reaction_type)
        self.db.add(reaction)
        await self.db.commit()
        return reaction

    async def schedule_stream(
        self,
        streamer_id: int,
        tenant_id: int,
        title: str,
        scheduled_start: datetime,
        description: str = None,
        scheduled_end: datetime = None,
        is_recurring: bool = False,
        recurrence_pattern: str = None,
    ) -> LiveStreamSchedule:
        """Schedule a live stream."""
        schedule = LiveStreamSchedule(
            streamer_id=streamer_id,
            tenant_id=tenant_id,
            title=title,
            description=description,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            is_recurring=is_recurring,
            recurrence_pattern=recurrence_pattern,
        )
        self.db.add(schedule)
        await self.db.commit()
        await self.db.refresh(schedule)
        return schedule

    async def get_upcoming_streams(self, tenant_id: int, limit: int = 20) -> list:
        """Get upcoming scheduled streams."""
        now = datetime.utcnow()
        query = select(LiveStreamSchedule).where(
            LiveStreamSchedule.tenant_id == tenant_id,
            LiveStreamSchedule.scheduled_start >= now,
        ).order_by(LiveStreamSchedule.scheduled_start.asc()).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_dvr_segment(
        self,
        stream_id: int,
        segment_url: str,
        start_time: datetime,
        end_time: datetime,
        segment_duration: int = 10,
    ) -> LiveStreamDVR:
        """Create a DVR segment for a stream."""
        dvr = LiveStreamDVR(
            stream_id=stream_id,
            segment_url=segment_url,
            segment_duration=segment_duration,
            start_time=start_time,
            end_time=end_time,
        )
        self.db.add(dvr)
        await self.db.commit()
        await self.db.refresh(dvr)
        return dvr

    async def get_dvr_segments(self, stream_id: int) -> list:
        """Get DVR segments for a stream."""
        query = select(LiveStreamDVR).where(
            LiveStreamDVR.stream_id == stream_id
        ).order_by(LiveStreamDVR.start_time.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_viewer_count(self, stream_id: int, viewer_count: int) -> Optional[LiveStream]:
        """Update viewer count for a stream."""
        stream = await self.db.get(LiveStream, stream_id)
        if stream:
            stream.viewer_count = viewer_count
            if viewer_count > stream.peak_viewers:
                stream.peak_viewers = viewer_count
            await self.db.commit()
        return stream

    async def subscribe_to_stream(
        self,
        stream_id: int,
        user_id: int,
        notification_type: str = "start",
        notify_before_minutes: int = 5,
    ) -> LiveStreamNotification:
        """Subscribe to stream notifications."""
        notification = LiveStreamNotification(
            stream_id=stream_id,
            user_id=user_id,
            notification_type=notification_type,
            notify_before_minutes=notify_before_minutes,
        )
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def get_stream_subscribers(self, stream_id: int) -> list:
        """Get users subscribed to a stream."""
        query = select(LiveStreamNotification).where(
            LiveStreamNotification.stream_id == stream_id
        )
        result = await self.db.execute(query)
        return result.scalars().all()
