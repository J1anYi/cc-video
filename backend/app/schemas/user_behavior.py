from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime


class JourneyEventResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    event_data: Optional[Dict[str, Any]] = None
    page_url: str
    referrer_url: Optional[str] = None
    created_at: str


class UserJourneyResponse(BaseModel):
    user_id: int
    events: List[JourneyEventResponse]
    total_events: int


class SessionMetricsResponse(BaseModel):
    total_sessions: int
    avg_duration_seconds: int
    bounce_rate: float
    peak_hour: int


class SegmentRule(BaseModel):
    field: str
    op: str
    value: Any


class SegmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    rules: Optional[List[SegmentRule]] = None
    member_count: int
    created_at: str


class CreateSegmentRequest(BaseModel):
    name: str
    description: Optional[str] = None
    rules: List[SegmentRule]


class CohortResponse(BaseModel):
    cohort_key: str
    signup_count: int
    d1_retention: Optional[float] = None
    d7_retention: Optional[float] = None
    d14_retention: Optional[float] = None
    d30_retention: Optional[float] = None


class ChurnRiskUserResponse(BaseModel):
    user_id: int
    email: str
    risk_score: float
    risk_factors: Optional[Dict[str, Any]] = None
    last_login_days: Optional[int] = None
