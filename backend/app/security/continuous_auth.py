"""Continuous Authentication Engine"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for sessions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SessionRisk:
    """Risk assessment for a session"""
    session_id: str
    user_id: int
    risk_score: float
    risk_level: RiskLevel
    risk_factors: List[str] = field(default_factory=list)
    last_assessment: datetime = field(default_factory=datetime.utcnow)
    requires_step_up: bool = False


class ContinuousAuthEngine:
    """Continuous Authentication Engine"""
    
    def __init__(
        self,
        trust_verifier=None,
        step_up_threshold: float = 0.7,
        critical_threshold: float = 0.3
    ):
        self.trust_verifier = trust_verifier
        self.step_up_threshold = step_up_threshold
        self.critical_threshold = critical_threshold
        self._session_risks: Dict[str, SessionRisk] = {}
        self._behavior_history: Dict[int, List[Dict[str, Any]]] = {}
    
    async def analyze_behavior(self, context: Any) -> float:
        """Analyze user behavior for anomalies"""
        user_id = context.user_id
        
        if self.trust_verifier:
            profile = await self.trust_verifier.get_behavior_profile(user_id)
        else:
            profile = {"risk_score": 0.5}
        
        base_score = 1.0 - profile.get("risk_score", 0.5)
        
        anomalies = await self._detect_anomalies(context)
        if anomalies:
            base_score *= 0.8 ** len(anomalies)
        
        return max(0, min(1, base_score))
    
    async def assess_session_risk(
        self,
        session_id: str,
        user_id: int,
        context: Optional[Any] = None
    ) -> SessionRisk:
        """Assess risk for a session"""
        if session_id in self._session_risks:
            risk = self._session_risks[session_id]
        else:
            risk = SessionRisk(
                session_id=session_id,
                user_id=user_id,
                risk_score=1.0,
                risk_level=RiskLevel.LOW
            )
            self._session_risks[session_id] = risk
        
        risk_factors = []
        risk_score = 1.0
        
        session_age = await self._get_session_age(session_id)
        if session_age > timedelta(hours=8):
            risk_factors.append("long_session")
            risk_score *= 0.9
        elif session_age > timedelta(hours=24):
            risk_factors.append("very_long_session")
            risk_score *= 0.7
        
        if context:
            request_rate = await self._get_request_rate(session_id)
            if request_rate > 100:
                risk_factors.append("high_request_rate")
                risk_score *= 0.8
            
            behavior_score = await self.analyze_behavior(context)
            if behavior_score < 0.5:
                risk_factors.append("anomalous_behavior")
                risk_score *= behavior_score
        
        risk_level = self._calculate_risk_level(risk_score)
        
        risk.risk_score = risk_score
        risk.risk_level = risk_level
        risk.risk_factors = risk_factors
        risk.last_assessment = datetime.utcnow()
        risk.requires_step_up = risk_score < self.step_up_threshold
        
        return risk
    
    def _calculate_risk_level(self, risk_score: float) -> RiskLevel:
        """Convert risk score to risk level"""
        if risk_score >= 0.7:
            return RiskLevel.LOW
        elif risk_score >= 0.5:
            return RiskLevel.MEDIUM
        elif risk_score >= 0.3:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    async def _detect_anomalies(self, context: Any) -> List[str]:
        """Detect behavioral anomalies"""
        anomalies = []
        user_id = context.user_id
        
        current_hour = datetime.utcnow().hour
        if user_id in self._behavior_history:
            history = self._behavior_history[user_id]
            typical_hours = self._get_typical_hours(history)
            
            if typical_hours and current_hour not in typical_hours:
                anomalies.append("unusual_time")
        
        return anomalies
    
    async def _get_session_age(self, session_id: str) -> timedelta:
        """Get session age"""
        return timedelta(minutes=30)
    
    async def _get_request_rate(self, session_id: str) -> float:
        """Get request rate for session"""
        return 10.0
    
    def _get_typical_hours(self, history: List[Dict[str, Any]]) -> List[int]:
        """Get typical activity hours from history"""
        if not history:
            return []
        
        hour_counts: Dict[int, int] = {}
        for entry in history:
            hour = entry.get("hour", 0)
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if not hour_counts:
            return []
        
        avg = sum(hour_counts.values()) / len(hour_counts)
        return [h for h, c in hour_counts.items() if c > avg]
    
    async def record_activity(
        self,
        user_id: int,
        session_id: str,
        activity_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record user activity for behavior analysis"""
        if user_id not in self._behavior_history:
            self._behavior_history[user_id] = []
        
        activity = {
            "session_id": session_id,
            "type": activity_type,
            "hour": datetime.utcnow().hour,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self._behavior_history[user_id].append(activity)
        
        if len(self._behavior_history[user_id]) > 100:
            self._behavior_history[user_id] = self._behavior_history[user_id][-100:]
    
    async def trigger_step_up(self, session_id: str, reason: str) -> Dict[str, Any]:
        """Trigger step-up authentication"""
        if session_id not in self._session_risks:
            return {"success": False, "reason": "session_not_found"}
        
        risk = self._session_risks[session_id]
        
        logger.info(f"Step-up auth triggered for session {session_id}: {reason}")
        
        return {
            "success": True,
            "session_id": session_id,
            "user_id": risk.user_id,
            "reason": reason,
            "current_risk_score": risk.risk_score,
            "required_action": "reauthenticate"
        }
    
    def get_high_risk_sessions(self) -> List[SessionRisk]:
        """Get all sessions with elevated risk"""
        return [
            risk for risk in self._session_risks.values()
            if risk.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
        ]
    
    async def terminate_high_risk_sessions(self) -> int:
        """Terminate all high-risk sessions"""
        terminated = 0
        for session_id, risk in list(self._session_risks.items()):
            if risk.risk_level == RiskLevel.CRITICAL:
                del self._session_risks[session_id]
                terminated += 1
                logger.info(f"Terminated critical risk session: {session_id}")
        
        return terminated
