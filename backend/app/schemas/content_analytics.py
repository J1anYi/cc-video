from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime


class ContentMetricsResponse(BaseModel):
    content_id: int
    title: str
    total_views: int
    unique_viewers: int
    avg_completion_pct: float
    total_watch_time_hours: float
    engagement_score: float
    last_updated: Optional[str] = None


class HeatmapDataPoint(BaseModel):
    timestamp_seconds: int
    engagement_pct: float
    play_count: int
    pause_count: int
    seek_count: int
    rewind_count: int


class HeatmapResponse(BaseModel):
    content_id: int
    duration_seconds: int
    samples: List[HeatmapDataPoint]


class DropOffPoint(BaseModel):
    timestamp_seconds: int
    drop_pct: float


class CompletionAnalysisResponse(BaseModel):
    content_id: int
    completion_rate: float
    avg_watch_duration_seconds: int
    drop_off_points: List[DropOffPoint]


class ContentComparisonItem(BaseModel):
    content_id: int
    title: str
    total_views: int
    unique_viewers: int
    avg_completion_pct: float
    engagement_score: float


class ContentComparisonResponse(BaseModel):
    items: List[ContentComparisonItem]


class TrendingContentItem(BaseModel):
    id: int
    title: str
    views_24h: int
    velocity: float
    momentum: float
    trending_score: float
    poster_url: Optional[str] = None


class TrendingContentResponse(BaseModel):
    content: List[TrendingContentItem]
    time_range: str
    generated_at: str
