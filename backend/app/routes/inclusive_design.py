"""Phase 193: Inclusive Design Routes"""
from fastapi import APIRouter, Body
from typing import List
from ..services.inclusive_design import InclusiveDesignService

router = APIRouter(prefix="/api/inclusive-design", tags=["inclusive-design"])
service = InclusiveDesignService()

@router.post("/languages")
async def expand_languages(languages: List[str] = Body(default=[])):
    return await service.expand_languages(languages)

@router.post("/rtl/{locale}")
async def enable_rtl(locale: str):
    return await service.enable_rtl_support(locale)

@router.post("/localize/{content_id}")
async def localize_content(content_id: str, region: str = "en-US"):
    return await service.localize_content(content_id, region)

@router.post("/age-mode/{user_id}")
async def set_age_mode(user_id: str, age_range: str = "adult"):
    return await service.set_age_mode(user_id, age_range)

@router.post("/family-profile/{user_id}")
async def create_family_profile(user_id: str):
    return await service.create_family_profile(user_id)
