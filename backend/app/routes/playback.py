from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas.playback import (
    PlaybackSettings, PlaybackSession, PlaybackQuality,
    DataSaverMode, BatteryStatus, AdaptiveBitrateInfo
)
from datetime import datetime
import uuid

router = APIRouter(prefix="/playback", tags=["playback"])

def get_current_user_id(x_user_id: str = Header(...)) -> int:
    return int(x_user_id)

@router.post("/sessions", response_model=PlaybackSession)
def create_session(
    movie_id: int,
    quality: PlaybackQuality = PlaybackQuality.AUTO,
    user_id: int = Depends(get_current_user_id)
):
    return PlaybackSession(
        session_id=str(uuid.uuid4()),
        movie_id=movie_id,
        quality=quality.value,
        position_seconds=0,
        duration_seconds=0,
        created_at=datetime.utcnow()
    )

@router.get("/adaptive/{movie_id}", response_model=AdaptiveBitrateInfo)
def get_adaptive_bitrate(
    movie_id: int,
    bandwidth: Optional[int] = None,
    battery_level: Optional[float] = None
):
    return AdaptiveBitrateInfo(
        current_bitrate=2500000,
        available_bitrates=[500000, 1000000, 2500000, 5000000],
        recommended_bitrate=2500000,
        reason="optimal_for_bandwidth"
    )

@router.get("/settings", response_model=PlaybackSettings)
def get_playback_settings(user_id: int = Depends(get_current_user_id)):
    return PlaybackSettings(
        quality=PlaybackQuality.AUTO,
        data_saver=DataSaverMode.OFF,
        audio_only=False,
        background_playback=True,
        pip_enabled=True
    )

@router.put("/settings", response_model=PlaybackSettings)
def update_playback_settings(
    settings: PlaybackSettings,
    user_id: int = Depends(get_current_user_id)
):
    return settings

@router.post("/sessions/{session_id}/pip")
def enable_pip(session_id: str):
    return {"pip_enabled": True, "session_id": session_id}

@router.post("/sessions/{session_id}/background")
def enable_background(session_id: str):
    return {"background_enabled": True, "session_id": session_id}
