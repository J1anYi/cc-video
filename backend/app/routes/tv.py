"""Smart TV API routes."""
from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services.tv_platform import TVPlatformService
from ..schemas.tv import (
    TVPlatform, TVDeviceInfo, TVSession, TVNavigationEvent,
    TVUIConfig, TVPlaybackSettings, TVVoiceCommand, TVRemoteKey
)

router = APIRouter(prefix="/tv", tags=["tv"])


def get_current_user_id(x_user_id: str = Header(...)) -> int:
    return int(x_user_id)


@router.post("/devices", response_model=TVSession)
def register_tv_device(
    device_info: TVDeviceInfo,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Register a TV device and create session."""
    service = TVPlatformService(db)
    return service.register_device(user_id, device_info)


@router.get("/platform/detect")
def detect_platform(request: Request, db: Session = Depends(get_db)):
    """Detect TV platform from user agent."""
    service = TVPlatformService(db)
    user_agent = request.headers.get("user-agent", "")
    platform = service.detect_platform(user_agent)
    return {"platform": platform.value, "user_agent": user_agent}


@router.get("/ui-config", response_model=TVUIConfig)
def get_ui_config(
    platform: TVPlatform = TVPlatform.ANDROID_TV,
    db: Session = Depends(get_db)
):
    """Get TV-specific UI configuration."""
    service = TVPlatformService(db)
    return service.get_ui_config(platform)


@router.post("/playback-settings", response_model=TVPlaybackSettings)
def get_playback_settings(
    device_info: TVDeviceInfo,
    db: Session = Depends(get_db)
):
    """Get playback settings for TV device."""
    service = TVPlatformService(db)
    return service.get_playback_settings(device_info.platform, device_info)


@router.post("/navigation")
def handle_navigation(
    event: TVNavigationEvent,
    session_id: str = Header(..., alias="X-TV-Session-ID"),
    db: Session = Depends(get_db)
):
    """Handle TV remote navigation event."""
    service = TVPlatformService(db)
    return service.handle_navigation(session_id, event)


@router.post("/voice")
def process_voice_command(
    command: TVVoiceCommand,
    db: Session = Depends(get_db)
):
    """Process voice command from TV remote."""
    service = TVPlatformService(db)
    return service.process_voice_command(command)


@router.get("/features")
def get_platform_features(
    platform: TVPlatform = TVPlatform.ANDROID_TV,
    db: Session = Depends(get_db)
):
    """Get available features for TV platform."""
    service = TVPlatformService(db)
    return {"platform": platform.value, "features": service.get_platform_features(platform)}


@router.get("/remote-keys")
def get_remote_key_mapping():
    """Get TV remote key mappings."""
    return {"keys": [key.value for key in TVRemoteKey]}
