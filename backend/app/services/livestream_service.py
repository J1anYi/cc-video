from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.livestream import LiveStream, LiveChat, StreamReaction, StreamStatus


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
