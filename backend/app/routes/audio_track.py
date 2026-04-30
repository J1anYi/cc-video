"""Audio track routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.audio_track_service import AudioTrackService
from app.models.audio_track import AudioChannelLayout


router = APIRouter(prefix="/audio-tracks", tags=["audio-tracks"])


class TrackCreate(BaseModel):
    video_file_id: int
    language: str
    file_path: str
    title: Optional[str] = None
    is_default: bool = False
    is_original: bool = False
    channel_layout: str = "stereo"
    codec: str = "aac"
    bitrate: int = 128000
    sample_rate: int = 48000


@router.post("")
async def create_track(
    data: TrackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create an audio track."""
    service = AudioTrackService(db)
    try:
        channel_enum = AudioChannelLayout(data.channel_layout)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid channel layout")
    
    track = await service.create_audio_track(
        video_file_id=data.video_file_id,
        language=data.language,
        file_path=data.file_path,
        title=data.title,
        is_default=data.is_default,
        is_original=data.is_original,
        channel_layout=channel_enum,
        codec=data.codec,
        bitrate=data.bitrate,
        sample_rate=data.sample_rate,
    )
    return {"id": track.id, "language": track.language}


@router.get("/video/{video_file_id}")
async def get_video_tracks(
    video_file_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get all audio tracks for a video file."""
    service = AudioTrackService(db)
    tracks = await service.get_tracks_for_video(video_file_id)
    return {
        "tracks": [
            {
                "id": t.id,
                "language": t.language,
                "title": t.title,
                "is_default": t.is_default,
                "is_original": t.is_original,
                "channel_layout": t.channel_layout.value,
                "codec": t.codec,
                "bitrate": t.bitrate,
            }
            for t in tracks
        ]
    }


@router.put("/{track_id}/default")
async def set_default_track(
    track_id: int,
    video_file_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Set an audio track as default."""
    service = AudioTrackService(db)
    track = await service.set_default_track(track_id, video_file_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"id": track.id, "is_default": True}


@router.delete("/{track_id}")
async def delete_track(
    track_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an audio track."""
    service = AudioTrackService(db)
    success = await service.delete_track(track_id)
    if not success:
        raise HTTPException(status_code=404, detail="Track not found")
    return {"message": "Track deleted"}
