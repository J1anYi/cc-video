"""Playback routes."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.services.playback_service import PlaybackService


router = APIRouter(prefix="/playback", tags=["playback"])


class SettingsUpdate(BaseModel):
    default_speed: Optional[float] = 1.0
    auto_skip_intro: Optional[bool] = True
    auto_skip_credits: Optional[bool] = False
    auto_next_episode: Optional[bool] = True
    pip_enabled: Optional[bool] = True
    keyboard_shortcuts: Optional[dict] = None


class ProgressSave(BaseModel):
    movie_id: int
    position_seconds: int
    duration_seconds: int


@router.get("/settings")
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PlaybackService(db)
    settings = await service.get_settings(current_user.id)
    if not settings:
        return {"default_speed": 1.0, "auto_skip_intro": True, "auto_skip_credits": False, "auto_next_episode": True, "pip_enabled": True, "keyboard_shortcuts": None}
    return {"default_speed": settings.default_speed, "auto_skip_intro": settings.auto_skip_intro, "auto_skip_credits": settings.auto_skip_credits, "auto_next_episode": settings.auto_next_episode, "pip_enabled": settings.pip_enabled, "keyboard_shortcuts": settings.keyboard_shortcuts}


@router.put("/settings")
async def update_settings(
    data: SettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = PlaybackService(db)
    await service.create_or_update_settings(
        user_id=current_user.id, tenant_id=tenant_id,
        default_speed=data.default_speed, auto_skip_intro=data.auto_skip_intro,
        auto_skip_credits=data.auto_skip_credits, auto_next_episode=data.auto_next_episode,
        pip_enabled=data.pip_enabled, keyboard_shortcuts=data.keyboard_shortcuts,
    )
    return {"message": "Settings updated"}


@router.post("/progress")
async def save_progress(
    data: ProgressSave,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = PlaybackService(db)
    progress = await service.save_progress(
        user_id=current_user.id, movie_id=data.movie_id, tenant_id=tenant_id,
        position_seconds=data.position_seconds, duration_seconds=data.duration_seconds,
    )
    return {"position_seconds": progress.position_seconds, "completion_percentage": progress.completion_percentage}


@router.get("/progress/{movie_id}")
async def get_progress(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PlaybackService(db)
    progress = await service.get_progress(current_user.id, movie_id)
    if not progress:
        return {"position_seconds": 0, "completion_percentage": 0}
    return {"position_seconds": progress.position_seconds, "duration_seconds": progress.duration_seconds, "completion_percentage": progress.completion_percentage}


@router.get("/progress")
async def get_all_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PlaybackService(db)
    progress_list = await service.get_all_progress(current_user.id)
    return {"progress": [{"movie_id": p.movie_id, "position_seconds": p.position_seconds, "duration_seconds": p.duration_seconds, "completion_percentage": p.completion_percentage} for p in progress_list]}
