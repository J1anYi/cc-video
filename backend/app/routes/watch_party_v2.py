from fastapi import APIRouter
from typing import Dict, Any
from app.services.watch_party import watch_party_service

router = APIRouter(prefix="/api/watch-party-v2", tags=["watch-party-v2"])

@router.post("/room")
async def create_room(host_id: str) -> Dict[str, Any]:
    return await watch_party_service.create_room(host_id)

@router.post("/room/{room_id}/join")
async def join_room(room_id: str, user_id: str) -> Dict[str, Any]:
    return await watch_party_service.add_participant(room_id, user_id)

@router.post("/room/{room_id}/sync")
async def sync_playback(room_id: str, position: int) -> Dict[str, Any]:
    return await watch_party_service.sync_playback(room_id, position)

@router.post("/room/{room_id}/react")
async def send_reaction(room_id: str, user_id: str, reaction: str) -> Dict[str, Any]:
    return await watch_party_service.send_reaction(room_id, user_id, reaction)

@router.post("/room/{room_id}/schedule")
async def schedule_party(room_id: str, scheduled_time: str) -> Dict[str, Any]:
    return await watch_party_service.schedule_party(room_id, scheduled_time)
