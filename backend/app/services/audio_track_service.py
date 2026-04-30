"""Audio track service."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audio_track import AudioTrack, AudioChannelLayout


class AudioTrackService:
    """Service for audio track operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_audio_track(
        self,
        video_file_id: int,
        language: str,
        file_path: str,
        title: str = None,
        is_default: bool = False,
        is_original: bool = False,
        channel_layout: AudioChannelLayout = AudioChannelLayout.STEREO,
        codec: str = "aac",
        bitrate: int = 128000,
        sample_rate: int = 48000,
    ) -> AudioTrack:
        """Create an audio track."""
        track = AudioTrack(
            video_file_id=video_file_id,
            language=language,
            title=title,
            is_default=is_default,
            is_original=is_original,
            channel_layout=channel_layout,
            codec=codec,
            bitrate=bitrate,
            sample_rate=sample_rate,
            file_path=file_path,
        )
        self.db.add(track)
        await self.db.commit()
        await self.db.refresh(track)
        return track

    async def get_tracks_for_video(self, video_file_id: int) -> List[AudioTrack]:
        """Get all audio tracks for a video file."""
        query = select(AudioTrack).where(
            AudioTrack.video_file_id == video_file_id
        ).order_by(AudioTrack.is_default.desc(), AudioTrack.language)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_track(self, track_id: int) -> Optional[AudioTrack]:
        """Get an audio track by ID."""
        return await self.db.get(AudioTrack, track_id)

    async def set_default_track(self, track_id: int, video_file_id: int) -> Optional[AudioTrack]:
        """Set an audio track as default for its video file."""
        query = select(AudioTrack).where(
            AudioTrack.video_file_id == video_file_id
        )
        result = await self.db.execute(query)
        tracks = result.scalars().all()
        for track in tracks:
            track.is_default = False
        
        track = await self.db.get(AudioTrack, track_id)
        if track and track.video_file_id == video_file_id:
            track.is_default = True
            await self.db.commit()
            await self.db.refresh(track)
            return track
        return None

    async def delete_track(self, track_id: int) -> bool:
        """Delete an audio track."""
        track = await self.db.get(AudioTrack, track_id)
        if track:
            await self.db.delete(track)
            await self.db.commit()
            return True
        return False
