from fastapi import APIRouter
from typing import Dict, Any
from app.services.ai_discovery import ai_discovery_service

router = APIRouter(prefix="/api/ai-discovery", tags=["ai-discovery"])

@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str) -> Dict[str, Any]:
    return await ai_discovery_service.get_recommendations(user_id)

@router.get("/for-you/{user_id}")
async def get_for_you_feed(user_id: str) -> Dict[str, Any]:
    return await ai_discovery_service.get_for_you_feed(user_id)

@router.get("/similar/{content_id}")
async def find_similar(content_id: str) -> Dict[str, Any]:
    return await ai_discovery_service.find_similar(content_id)

@router.get("/trending")
async def get_trending() -> Dict[str, Any]:
    return await ai_discovery_service.get_trending()

@router.post("/classify/{content_id}")
async def classify_content(content_id: str) -> Dict[str, Any]:
    return await ai_discovery_service.classify_content(content_id)
