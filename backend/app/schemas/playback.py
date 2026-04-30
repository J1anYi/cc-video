from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PlaybackQuality(str, Enum):
    AUTO = "auto"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class DataSaverMode(str, Enum):
    OFF = "off"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class BatteryStatus(BaseModel):
    level: float
    is_charging: bool
    is_low_power: bool

class PlaybackSettings(BaseModel):
    quality: PlaybackQuality
    data_saver: DataSaverMode
    audio_only: bool
    background_playback: bool
    pip_enabled: bool
    quality_cap_cellular: Optional[int] = 720
    quality_cap_wifi: Optional[int] = 1080

class PlaybackSession(BaseModel):
    session_id: str
    movie_id: int
    quality: str
    position_seconds: int
    duration_seconds: int
    bandwidth: Optional[int] = None
    battery_status: Optional[BatteryStatus] = None
    created_at: datetime

class AdaptiveBitrateInfo(BaseModel):
    current_bitrate: int
    available_bitrates: List[int]
    recommended_bitrate: int
    reason: str
