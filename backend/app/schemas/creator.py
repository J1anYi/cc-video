"""Creator platform schemas."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class CreatorProfileBase(BaseModel):
    channel_name: str
    channel_description: Optional[str] = None
    channel_art_url: Optional[str] = None


class CreatorProfileCreate(CreatorProfileBase):
    pass


class CreatorProfileUpdate(BaseModel):
    channel_name: Optional[str] = None
    channel_description: Optional[str] = None
    channel_art_url: Optional[str] = None
    monetization_enabled: Optional[bool] = None


class CreatorProfileResponse(CreatorProfileBase):
    id: int
    user_id: int
    subscriber_count: int
    total_views: int
    total_watch_time: int
    is_verified: bool
    is_partner: bool
    monetization_enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreatorContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_type: str = "video"
    tags: List[str] = []
    metadata: dict = {}


class CreatorContentCreate(CreatorContentBase):
    movie_id: Optional[int] = None
    thumbnail_url: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class CreatorContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


class CreatorContentResponse(CreatorContentBase):
    id: int
    creator_id: int
    movie_id: Optional[int]
    status: str
    thumbnail_url: Optional[str]
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentAnalyticsResponse(BaseModel):
    content_id: int
    views: int
    unique_viewers: int
    average_watch_time: float
    likes: int
    dislikes: int
    comments: int
    shares: int
    estimated_revenue: float
    demographics: dict
    traffic_sources: dict
    updated_at: datetime

    class Config:
        from_attributes = True


class CreatorDashboardResponse(BaseModel):
    profile: CreatorProfileResponse
    total_views: int
    total_subscribers: int
    total_watch_time: int
    estimated_revenue: float
    recent_content: List[CreatorContentResponse]
    top_content: List[CreatorContentResponse]
    audience_growth: dict
    engagement_rate: float


class TeamMemberInvite(BaseModel):
    email: str
    role: str = "viewer"
    permissions: List[str] = []


class TeamMemberResponse(BaseModel):
    id: int
    user_id: int
    role: str
    permissions: List[str]
    invited_at: datetime
    joined_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class CreatorEarningsResponse(BaseModel):
    id: int
    period_start: datetime
    period_end: datetime
    ad_revenue: float
    subscription_revenue: float
    tip_revenue: float
    total_revenue: float
    platform_fee: float
    net_revenue: float
    status: str
    payout_date: Optional[datetime]

    class Config:
        from_attributes = True
