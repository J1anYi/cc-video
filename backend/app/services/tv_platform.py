"""Smart TV platform service."""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid
from ..schemas.tv import (
    TVPlatform, TVDeviceInfo, TVSession, TVNavigationEvent,
    TVUIConfig, TVPlaybackSettings, TVVoiceCommand, TVRemoteKey
)


class TVPlatformService:
    """Service for smart TV platform operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def detect_platform(self, user_agent: str) -> TVPlatform:
        """Detect TV platform from user agent."""
        ua_lower = user_agent.lower()
        
        if "tizen" in ua_lower or "samsung" in ua_lower:
            return TVPlatform.TIZEN
        elif "webos" in ua_lower or "lg" in ua_lower:
            return TVPlatform.WEBOS
        elif "android tv" in ua_lower or "google tv" in ua_lower:
            return TVPlatform.ANDROID_TV
        elif "appletv" in ua_lower or "tvos" in ua_lower:
            return TVPlatform.TVOS
        elif "roku" in ua_lower:
            return TVPlatform.ROKU
        
        return TVPlatform.ANDROID_TV
    
    def register_device(
        self, 
        user_id: int, 
        device_info: TVDeviceInfo
    ) -> TVSession:
        """Register a TV device and create session."""
        session = TVSession(
            session_id=str(uuid.uuid4()),
            device_id=device_info.device_id,
            platform=device_info.platform,
            user_id=user_id,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        return session
    
    def get_ui_config(self, platform: TVPlatform) -> TVUIConfig:
        """Get platform-specific UI configuration."""
        base_config = TVUIConfig()
        
        if platform == TVPlatform.TVOS:
            base_config.focus_highlight_color = "#ffffff"
        elif platform == TVPlatform.ROKU:
            base_config.font_scale = 1.3
        
        return base_config
    
    def get_playback_settings(
        self, 
        platform: TVPlatform,
        device_info: TVDeviceInfo
    ) -> TVPlaybackSettings:
        """Get playback settings for TV device."""
        return TVPlaybackSettings(
            preferred_resolution=2160 if device_info.hdr_capable else 1080,
            hdr_enabled=device_info.hdr_capable,
            dolby_vision_enabled=device_info.dolby_vision,
            dolby_atmos_enabled=device_info.dolby_atmos,
            frame_rate_matching=True
        )
    
    def handle_navigation(
        self, 
        session_id: str, 
        event: TVNavigationEvent
    ) -> Dict[str, Any]:
        """Handle TV remote navigation event."""
        return {
            "action": "navigate",
            "key": event.key.value,
            "timestamp": event.timestamp.isoformat()
        }
    
    def process_voice_command(
        self, 
        command: TVVoiceCommand
    ) -> Dict[str, Any]:
        """Process voice command from TV remote."""
        return {
            "understood": True,
            "action": "search",
            "query": command.command
        }
    
    def get_platform_features(self, platform: TVPlatform) -> List[str]:
        """Get available features for platform."""
        features = ["streaming", "playback_controls", "search"]
        
        if platform in [TVPlatform.TIZEN, TVPlatform.WEBOS, TVPlatform.ANDROID_TV]:
            features.extend(["voice_search", "smart_home"])
        
        if platform in [TVPlatform.TVOS, TVPlatform.ANDROID_TV]:
            features.append("multi_user")
        
        if platform == TVPlatform.TVOS:
            features.append("airplay")
        
        return features
