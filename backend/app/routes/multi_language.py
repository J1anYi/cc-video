"""Phase 201: Multi-Language Platform Routes"""
from fastapi import APIRouter
from ..services.multi_language import MultiLanguageService

router = APIRouter(prefix="/api/multi-language", tags=["multi-language"])
service = MultiLanguageService()

@router.post("/content/{content_id}")
async def manage_content(content_id: str, language_data: dict):
    return await service.manage_content_language(content_id, language_data)

@router.post("/switch/{user_id}")
async def switch_lang(user_id: str, language: str):
    return await service.switch_language(user_id, language)

@router.post("/subtitles/{video_id}")
async def manage_subs(video_id: str, subtitle_config: dict):
    return await service.manage_subtitles(video_id, subtitle_config)

@router.post("/adapt/{content_id}")
async def adapt_content(content_id: str, region: str):
    return await service.adapt_cultural_content(content_id, region)

@router.get("/analytics/{tenant_id}")
async def get_analytics(tenant_id: str):
    return await service.get_language_analytics(tenant_id)
