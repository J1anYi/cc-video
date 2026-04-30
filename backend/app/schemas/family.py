"""Family and kids safety schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time
from enum import Enum


class AgeRating(str, Enum):
    ALL = "all"
    G = "g"
    PG = "pg"
    PG13 = "pg13"
    R = "r"
    NC17 = "nc17"


class ProfileType(str, Enum):
    ADULT = "adult"
    TEEN = "teen"
    KID = "kid"


class ScreenTimeLimit(BaseModel):
    daily_limit_minutes: int
    bedtime_start: Optional[time] = None
    bedtime_end: Optional[time] = None
    weekend_limit_minutes: Optional[int] = None


class ParentalControls(BaseModel):
    max_age_rating: AgeRating = AgeRating.PG
    block_unrated_content: bool = True
    require_pin_for_profiles: bool = True
    require_pin_for_purchases: bool = True
    allow_search: bool = True
    restrict_search_results: bool = True


class ContentBlock(BaseModel):
    movie_id: int
    reason: Optional[str] = None
    blocked_at: datetime


class ContentAllowItem(BaseModel):
    movie_id: int
    allowed_by: int
    allowed_at: datetime


class FamilyProfile(BaseModel):
    profile_id: int
    user_id: int
    name: str
    profile_type: ProfileType
    avatar_url: Optional[str] = None
    age: Optional[int] = None
    parental_controls: Optional[ParentalControls] = None
    screen_time_limit: Optional[ScreenTimeLimit] = None


class FamilyAccount(BaseModel):
    family_id: int
    owner_id: int
    name: str
    max_profiles: int = 6
    profiles: List[FamilyProfile]
    created_at: datetime


class ScreenTimeUsage(BaseModel):
    profile_id: int
    date: datetime
    minutes_watched: int
    limit_minutes: int
    remaining_minutes: int


class KidSafeMode(BaseModel):
    enabled: bool
    restricted_interface: bool = True
    hide_search: bool = True
    show_only_allowed: bool = False
