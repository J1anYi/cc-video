"""Phase 197: Content Upload Routes"""
from fastapi import APIRouter, Body
from typing import List, Dict, Any
from ..services.content_upload import ContentUploadService

router = APIRouter(prefix="/api/content-upload", tags=["content-upload"])
service = ContentUploadService()

@router.post("/session/{creator_id}")
async def create_session(creator_id: str, files: List[str] = Body(default=[])):
    return await service.create_upload_session(creator_id, files)

@router.put("/edit/{video_id}")
async def edit_video(video_id: str, edits: dict):
    return await service.edit_video(video_id, edits)

@router.post("/bulk/{creator_id}")
async def bulk_manage(creator_id: str, operation: str, content_ids: list):
    return await service.bulk_manage(creator_id, operation, content_ids)

@router.post("/version/{video_id}")
async def create_version(video_id: str, note: str):
    return await service.create_version(video_id, note)

@router.post("/template/{content_id}")
async def apply_template(content_id: str, template_id: str):
    return await service.apply_template(content_id, template_id)
