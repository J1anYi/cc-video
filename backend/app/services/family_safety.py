from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, time
from ..schemas.family import ParentalControls, ScreenTimeLimit, FamilyProfile, FamilyAccount, ScreenTimeUsage, KidSafeMode, ProfileType, AgeRating

class FamilySafetyService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_family_account(self, owner_id: int, name: str) -> FamilyAccount:
        return FamilyAccount(family_id=1, owner_id=owner_id, name=name, max_profiles=6, profiles=[], created_at=datetime.utcnow())
    
    def add_family_profile(self, family_id: int, name: str, profile_type: ProfileType, age: Optional[int] = None) -> FamilyProfile:
        profile = FamilyProfile(profile_id=1, user_id=1, name=name, profile_type=profile_type, age=age)
        if profile_type == ProfileType.KID:
            profile.parental_controls = ParentalControls(max_age_rating=AgeRating.PG)
            profile.screen_time_limit = ScreenTimeLimit(daily_limit_minutes=120)
        return profile
    
    def update_parental_controls(self, profile_id: int, controls: ParentalControls) -> ParentalControls:
        return controls
    
    def set_screen_time_limit(self, profile_id: int, limit: ScreenTimeLimit) -> ScreenTimeLimit:
        return limit
    
    def block_content(self, profile_id: int, movie_id: int, reason: Optional[str] = None) -> bool:
        return True
    
    def get_screen_time_usage(self, profile_id: int, date: Optional[datetime] = None) -> ScreenTimeUsage:
        return ScreenTimeUsage(profile_id=profile_id, date=date or datetime.utcnow(), minutes_watched=60, limit_minutes=120, remaining_minutes=60)
    
    def enable_kid_safe_mode(self, profile_id: int, settings: KidSafeMode) -> KidSafeMode:
        return settings
    
    def check_purchase_allowed(self, profile_id: int, amount: float) -> bool:
        return False
