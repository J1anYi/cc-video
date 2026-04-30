from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Dict, Any

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.sync import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])

class DeviceRegister(BaseModel):
    device_id: str
    device_name: str
    platform: str

class WatchHistorySync(BaseModel):
    movie_id: int
    watched_at: str
    completed: bool
    updated_at: str

class PlaybackPositionSync(BaseModel):
    movie_id: int
    position: int

class PreferencesSync(BaseModel):
    preferences: Dict[str, Any]

@router.post("/devices")
async def register_device(data: DeviceRegister, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync = SyncService(db)
    return await sync.register_device(current_user.id, data.device_id, data.device_name, data.platform)

@router.get("/devices")
async def get_devices(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync = SyncService(db)
    return {"devices": await sync.get_devices(current_user.id)}

@router.get("/state/{device_id}")
async def get_sync_state(device_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync = SyncService(db)
    return await sync.get_device_sync_state(current_user.id, device_id)

@router.post("/watch-history")
async def sync_watch_history(data: List[WatchHistorySync], device_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync = SyncService(db)
    items = [item.dict() for item in data]
    return await sync.sync_watch_history(current_user.id, device_id, items)

@router.post("/playback-position")
async def sync_playback_position(data: PlaybackPositionSync, device_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync = SyncService(db)
    return await sync.sync_playback_position(current_user.id, data.movie_id, data.position, device_id)

@router.post("/preferences")
async def sync_preferences(data: PreferencesSync, device_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sync = SyncService(db)
    return await sync.sync_preferences(current_user.id, data.preferences, device_id)
