from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime


class WatchTimeStats(BaseModel):
    total_hours: float
    total_movies: int


class AnalyticsResponse(BaseModel):
    watch_time: WatchTimeStats
    genre_breakdown: Dict[str, int]
    hourly_pattern: Dict[str, int]
    daily_pattern: Dict[str, int]
    last_updated: Optional[str] = None


class ActivityItem(BaseModel):
    id: int
    type: str
    movie_id: Optional[int] = None
    created_at: str


class ActivityTimelineResponse(BaseModel):
    activities: List[ActivityItem]
    total: int


class ExportDataResponse(BaseModel):
    export_date: str
    user_id: int
    watch_history: List[Dict[str, Any]]
    analytics: Dict[str, Any]
