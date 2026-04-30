"""Phase 199: Creator Community Routes"""
from fastapi import APIRouter
from ..services.creator_community import CreatorCommunityService

router = APIRouter(prefix="/api/creator-community", tags=["creator-community"])
service = CreatorCommunityService()

@router.post("/collaboration/{creator_id}")
async def create_collab(creator_id: str, collab_data: dict):
    return await service.create_collaboration(creator_id, collab_data)

@router.post("/message/{creator_id}")
async def send_msg(creator_id: str, message: dict):
    return await service.send_message(creator_id, message)

@router.post("/circle/{creator_id}")
async def create_circle(creator_id: str, circle_data: dict):
    return await service.create_circle(creator_id, circle_data)

@router.post("/moderation/{creator_id}")
async def setup_mod(creator_id: str, mod_config: dict):
    return await service.setup_moderation(creator_id, mod_config)

@router.post("/spotlight/{creator_id}")
async def spotlight(creator_id: str, reason: str):
    return await service.spotlight_creator(creator_id, reason)
