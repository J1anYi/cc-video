"""Phase 192: Adaptive Streaming Routes"""
from fastapi import APIRouter
from ..services.adaptive_streaming import AdaptiveStreamingService

router = APIRouter(prefix="/api/adaptive-streaming", tags=["adaptive-streaming"])
service = AdaptiveStreamingService()

@router.post("/bitrate/{user_id}")
async def configure_bitrate(user_id: str, bandwidth: str = "auto"):
    return await service.configure_adaptive_bitrate(user_id, bandwidth)

@router.post("/audio-description/{video_id}")
async def add_audio_description(video_id: str):
    return await service.add_audio_description(video_id)

@router.post("/sign-language/{video_id}")
async def enable_sign_language(video_id: str, language: str = "asl"):
    return await service.enable_sign_language_overlay(video_id, language)

@router.post("/sensitivity-warnings/{content_id}")
async def add_warnings(content_id: str, warnings: list = []):
    return await service.add_sensitivity_warnings(content_id, warnings)

@router.post("/reduced-motion/{user_id}")
async def enable_reduced_motion(user_id: str):
    return await service.apply_reduced_motion(user_id)
