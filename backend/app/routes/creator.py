"""Creator platform routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.creator import CreatorProfile, CreatorContent, CreatorContentAnalytics
from app.schemas.creator import (
    CreatorProfileCreate, CreatorProfileUpdate, CreatorProfileResponse,
    CreatorContentCreate, CreatorContentUpdate, CreatorContentResponse,
    ContentAnalyticsResponse, CreatorDashboardResponse,
    TeamMemberInvite, TeamMemberResponse
)
from app.services.creator import CreatorService

router = APIRouter(prefix="/creator", tags=["creator"])


@router.post("/profile", response_model=CreatorProfileResponse)
def create_profile(
    profile_data: CreatorProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = CreatorService.get_profile(db, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    return CreatorService.create_profile(db, current_user.id, profile_data)


@router.get("/profile", response_model=CreatorProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = CreatorService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/profile", response_model=CreatorProfileResponse)
def update_profile(
    update_data: CreatorProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = CreatorService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return CreatorService.update_profile(db, profile.id, update_data)


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dashboard = CreatorService.get_dashboard(db, current_user.id)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Profile not found")
    return dashboard


@router.post("/content", response_model=CreatorContentResponse)
def create_content(
    content_data: CreatorContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = CreatorService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return CreatorService.create_content(db, profile.id, content_data)


@router.get("/content", response_model=List[CreatorContentResponse])
def get_content(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = CreatorService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return CreatorService.get_content(db, profile.id, status)


@router.get("/content/{content_id}", response_model=CreatorContentResponse)
def get_single_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = db.query(CreatorContent).filter(CreatorContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.put("/content/{content_id}", response_model=CreatorContentResponse)
def update_content(
    content_id: int,
    update_data: CreatorContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CreatorService.update_content(db, content_id, update_data)


@router.get("/content/{content_id}/analytics", response_model=ContentAnalyticsResponse)
def get_content_analytics(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analytics = CreatorService.get_analytics(db, content_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    return analytics


@router.post("/team/invite", response_model=TeamMemberResponse)
def invite_team_member(
    invite_data: TeamMemberInvite,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = CreatorService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    member = CreatorService.invite_team_member(db, profile.id, invite_data)
    if not member:
        raise HTTPException(status_code=404, detail="User not found")
    return member


@router.get("/team", response_model=List[TeamMemberResponse])
def get_team_members(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = CreatorService.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return CreatorService.get_team_members(db, profile.id)
