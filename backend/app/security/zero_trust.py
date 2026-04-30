"""Zero Trust Security Engine - Core implementation"""
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class TrustLevel(Enum):
    """Trust levels for zero trust evaluation"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    FULL = 4


@dataclass
class TrustContext:
    """Context for trust evaluation"""
    user_id: int
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    request_count: int = 0
    last_activity: Optional[datetime] = None
    risk_factors: List[str] = field(default_factory=list)
    trust_score: float = 0.0
    
    def add_risk_factor(self, factor: str) -> None:
        """Add a risk factor to the context"""
        self.risk_factors.append(factor)
        self.trust_score = max(0, self.trust_score - 0.2)


class ZeroTrustEngine:
    """
    Zero Trust Security Engine
    Implements continuous verification and least-privilege access
    """
    
    MIN_TRUST_SCORE = 0.5
    STEP_UP_THRESHOLD = 0.7
    
    def __init__(self, trust_verifier=None, continuous_auth=None):
        self.trust_verifier = trust_verifier
        self.continuous_auth = continuous_auth
        self._active_sessions: Dict[str, TrustContext] = {}
    
    async def evaluate_trust(self, context: TrustContext) -> TrustLevel:
        """
        Evaluate trust level based on context
        Returns the appropriate trust level for the request
        """
        score = await self._calculate_trust_score(context)
        context.trust_score = score
        
        if score >= 0.9:
            return TrustLevel.FULL
        elif score >= 0.7:
            return TrustLevel.HIGH
        elif score >= 0.5:
            return TrustLevel.MEDIUM
        elif score >= 0.3:
            return TrustLevel.LOW
        else:
            return TrustLevel.NONE
    
    async def _calculate_trust_score(self, context: TrustContext) -> float:
        """Calculate trust score from multiple factors"""
        score = 1.0
        
        # Device verification
        if context.device_id:
            device_trust = await self._verify_device(context.device_id)
            score *= device_trust
        else:
            score *= 0.5
            context.add_risk_factor("unknown_device")
        
        # Location check
        if context.location:
            location_trust = await self._verify_location(context)
            score *= location_trust
        
        # Behavioral analysis
        if self.continuous_auth:
            behavior_score = await self.continuous_auth.analyze_behavior(context)
            score *= behavior_score
        
        # Session validity
        if context.session_id:
            session_trust = await self._verify_session(context.session_id)
            score *= session_trust
        
        return max(0, min(1, score))
    
    async def _verify_device(self, device_id: str) -> float:
        """Verify device trustworthiness"""
        # Known devices get higher trust
        # In production, check device registry
        known_devices = {"trusted_device_1", "trusted_device_2"}
        if device_id in known_devices:
            return 1.0
        return 0.7
    
    async def _verify_location(self, context: TrustContext) -> float:
        """Verify location-based trust"""
        if not context.location:
            return 0.8
        
        # Check for impossible travel
        # In production, compare with historical locations
        return 1.0
    
    async def _verify_session(self, session_id: str) -> float:
        """Verify session validity"""
        if session_id in self._active_sessions:
            return 1.0
        return 0.6
    
    def requires_step_up(self, context: TrustContext, required_level: TrustLevel) -> bool:
        """Check if step-up authentication is required"""
        current_level = TrustLevel.NONE
        for level in TrustLevel:
            if context.trust_score >= level.value * 0.25:
                current_level = level
        return current_level.value < required_level.value
    
    async def register_session(self, session_id: str, context: TrustContext) -> None:
        """Register a new session"""
        self._active_sessions[session_id] = context
        logger.info(f"Session registered: {session_id} for user {context.user_id}")
    
    async def revoke_session(self, session_id: str) -> None:
        """Revoke a session"""
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]
            logger.info(f"Session revoked: {session_id}")
    
    def get_active_sessions(self, user_id: int) -> List[TrustContext]:
        """Get all active sessions for a user"""
        return [
            ctx for ctx in self._active_sessions.values()
            if ctx.user_id == user_id
        ]
