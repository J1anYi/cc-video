from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..services.family_safety import FamilySafetyService
from ..schemas.family import (
    ParentalControls, ScreenTimeLimit, FamilyProfile,
    FamilyAccount, ScreenTimeUsage, KidSafeMode, ProfileType
)

router = APIRouter(prefix="/family", tags=["family"])

def get_current_user_id(x_user_id: str = Header(...)) -> int:
    return int(x_user_id)

@router.post("/accounts", response_model=FamilyAccount)
def create_family_account(name: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return service.create_family_account(user_id, name)

@router.post("/profiles", response_model=FamilyProfile)
def add_family_profile(family_id: int, name: str, profile_type: ProfileType, age: Optional[int] = None, db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return service.add_family_profile(family_id, name, profile_type, age)

@router.put("/profiles/{profile_id}/controls", response_model=ParentalControls)
def update_controls(profile_id: int, controls: ParentalControls, db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return service.update_parental_controls(profile_id, controls)

@router.put("/profiles/{profile_id}/screen-time", response_model=ScreenTimeLimit)
def set_screen_time(profile_id: int, limit: ScreenTimeLimit, db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return service.set_screen_time_limit(profile_id, limit)

@router.get("/profiles/{profile_id}/usage", response_model=ScreenTimeUsage)
def get_usage(profile_id: int, db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return service.get_screen_time_usage(profile_id)

@router.post("/profiles/{profile_id}/block/{movie_id}")
def block_movie(profile_id: int, movie_id: int, reason: Optional[str] = None, db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return {"blocked": service.block_content(profile_id, movie_id, reason)}

@router.put("/profiles/{profile_id}/kid-safe-mode", response_model=KidSafeMode)
def set_kid_safe_mode(profile_id: int, settings: KidSafeMode, db: Session = Depends(get_db)):
    service = FamilySafetyService(db)
    return service.enable_kid_safe_mode(profile_id, settings)
