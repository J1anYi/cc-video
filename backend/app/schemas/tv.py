"""Smart TV platform schemas."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TVPlatform(str, Enum):
    TIZEN = "tizen"           # Samsung
    WEBOS = "webos"           # LG
    ANDROID_TV = "android_tv" # Android TV/Google TV
    TVOS = "tvos"             # Apple TV
    ROKU = "roku"             # Roku


class TVRemoteKey(str, Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    SELECT = "select"
    BACK = "back"
    HOME = "home"
    MENU = "menu"
    PLAY = "play"
    PAUSE = "pause"
    REWIND = "rewind"
    FORWARD = "forward"
    VOICE = "voice"


class TVDeviceInfo(BaseModel):
    platform: TVPlatform
    device_id: str
    device_name: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    app_version: Optional[str] = None
    screen_resolution: Optional[str] = None
    hdr_capable: bool = False
    dolby_vision: bool = False
    dolby_atmos: bool = False


class TVSession(BaseModel):
    session_id: str
    device_id: str
    platform: TVPlatform
    user_id: int
    created_at: datetime
    last_active: datetime


class TVNavigationEvent(BaseModel):
    key: TVRemoteKey
    timestamp: datetime
    context: Optional[str] = None


class TVUIConfig(BaseModel):
    safe_area_horizontal: int = 90  # pixels from edge
    safe_area_vertical: int = 45
    focus_highlight_color: str = "#e50914"
    font_scale: float = 1.5
    item_spacing: int = 30
    carousel_item_width: int = 300
    carousel_item_height: int = 450


class TVPlaybackSettings(BaseModel):
    preferred_resolution: int = 2160  # 4K default
    hdr_enabled: bool = True
    dolby_vision_enabled: bool = True
    dolby_atmos_enabled: bool = True
    frame_rate_matching: bool = True


class TVVoiceCommand(BaseModel):
    command: str
    language: str = "en-US"
    confidence: Optional[float] = None
