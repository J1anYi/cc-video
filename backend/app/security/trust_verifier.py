"""Trust Verifier - Device and behavior verification"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class DeviceFingerprint:
    """Device fingerprint for trust verification"""
    device_id: str
    user_agent: str
    platform: str
    browser: str
    first_seen: datetime
    last_seen: datetime
    trust_score: float
    is_verified: bool


class TrustVerifier:
    """
    Verifies trust for devices, locations, and behavior
    """
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self._device_registry: Dict[str, DeviceFingerprint] = {}
        self._location_history: Dict[int, List[Dict[str, Any]]] = {}
        self._behavior_profiles: Dict[int, Dict[str, Any]] = {}
    
    async def verify_device(
        self,
        device_id: str,
        user_agent: str,
        user_id: int
    ) -> float:
        """
        Verify device trustworthiness
        Returns a trust score between 0 and 1
        """
        # Check if device is known
        if device_id in self._device_registry:
            device = self._device_registry[device_id]
            
            # Update last seen
            device.last_seen = datetime.utcnow()
            
            # Check if user agent matches
            if device.user_agent != user_agent:
                logger.warning(
                    f"User agent mismatch for device {device_id}"
                )
                return device.trust_score * 0.7
            
            return device.trust_score
        
        # New device - lower trust initially
        return 0.5
    
    async def register_device(
        self,
        device_id: str,
        user_agent: str,
        user_id: int,
        verify: bool = False
    ) -> DeviceFingerprint:
        """Register a new device"""
        now = datetime.utcnow()
        
        # Parse user agent for platform/browser
        platform = self._parse_platform(user_agent)
        browser = self._parse_browser(user_agent)
        
        fingerprint = DeviceFingerprint(
            device_id=device_id,
            user_agent=user_agent,
            platform=platform,
            browser=browser,
            first_seen=now,
            last_seen=now,
            trust_score=0.5 if not verify else 0.8,
            is_verified=verify
        )
        
        self._device_registry[device_id] = fingerprint
        logger.info(f"Device registered: {device_id} for user {user_id}")
        
        return fingerprint
    
    async def verify_location(
        self,
        user_id: int,
        ip_address: str,
        location: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Verify location trustworthiness
        Checks for impossible travel and unusual locations
        """
        if user_id not in self._location_history:
            # First location for user
            self._location_history[user_id] = [{
                "ip": ip_address,
                "location": location,
                "timestamp": datetime.utcnow()
            }]
            return 0.7
        
        history = self._location_history[user_id]
        last_entry = history[-1]
        
        # Check for impossible travel
        if location and last_entry.get("location"):
            is_impossible = await self._check_impossible_travel(
                last_entry["location"],
                location,
                last_entry["timestamp"]
            )
            if is_impossible:
                logger.warning(
                    f"Impossible travel detected for user {user_id}"
                )
                return 0.2
        
        # Update history
        history.append({
            "ip": ip_address,
            "location": location,
            "timestamp": datetime.utcnow()
        })
        
        # Keep only last 10 entries
        if len(history) > 10:
            self._location_history[user_id] = history[-10:]
        
        return 0.9
    
    async def _check_impossible_travel(
        self,
        from_location: Dict[str, Any],
        to_location: Dict[str, Any],
        from_time: datetime
    ) -> bool:
        """Check if travel between locations is impossible"""
        # Calculate distance and time
        # For simplicity, use lat/lng if available
        if not all([
            from_location.get("lat"),
            from_location.get("lng"),
            to_location.get("lat"),
            to_location.get("lng")
        ]):
            return False
        
        # Calculate approximate distance (km)
        from_lat = from_location["lat"]
        from_lng = from_location["lng"]
        to_lat = to_location["lat"]
        to_lng = to_location["lng"]
        
        # Simplified distance calculation
        lat_diff = abs(from_lat - to_lat)
        lng_diff = abs(from_lng - to_lng)
        distance = (lat_diff**2 + lng_diff**2)**0.5 * 111  # rough km
        
        # Time difference
        time_diff = datetime.utcnow() - from_time
        hours = time_diff.total_seconds() / 3600
        
        if hours == 0:
            return distance > 100  # 100km instant travel
        
        # Speed in km/h
        speed = distance / hours
        
        # Impossible if speed > 1000 km/h (commercial flight speed)
        return speed > 1000
    
    def _parse_platform(self, user_agent: str) -> str:
        """Parse platform from user agent"""
        ua_lower = user_agent.lower()
        if "windows" in ua_lower:
            return "Windows"
        elif "mac" in ua_lower:
            return "macOS"
        elif "linux" in ua_lower:
            return "Linux"
        elif "android" in ua_lower:
            return "Android"
        elif "ios" in ua_lower or "iphone" in ua_lower or "ipad" in ua_lower:
            return "iOS"
        return "Unknown"
    
    def _parse_browser(self, user_agent: str) -> str:
        """Parse browser from user agent"""
        ua_lower = user_agent.lower()
        if "edg" in ua_lower:
            return "Edge"
        elif "chrome" in ua_lower:
            return "Chrome"
        elif "firefox" in ua_lower:
            return "Firefox"
        elif "safari" in ua_lower:
            return "Safari"
        return "Unknown"
    
    async def get_behavior_profile(
        self,
        user_id: int
    ) -> Dict[str, Any]:
        """Get behavior profile for a user"""
        if user_id not in self._behavior_profiles:
            return {
                "avg_request_interval": 0,
                "common_paths": [],
                "typical_hours": [],
                "risk_score": 0.5
            }
        return self._behavior_profiles[user_id]
    
    async def update_behavior_profile(
        self,
        user_id: int,
        request_path: str
    ) -> None:
        """Update behavior profile with new request"""
        if user_id not in self._behavior_profiles:
            self._behavior_profiles[user_id] = {
                "request_count": 0,
                "paths": {},
                "hours": {},
                "last_update": datetime.utcnow()
            }
        
        profile = self._behavior_profiles[user_id]
        profile["request_count"] += 1
        profile["paths"][request_path] = profile["paths"].get(request_path, 0) + 1
        
        hour = datetime.utcnow().hour
        profile["hours"][hour] = profile["hours"].get(hour, 0) + 1
        profile["last_update"] = datetime.utcnow()
