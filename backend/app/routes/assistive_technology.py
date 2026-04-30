"""Phase 194: Assistive Technology Routes"""
from fastapi import APIRouter
from ..services.assistive_technology import AssistiveTechnologyService

router = APIRouter(prefix="/api/assistive-tech", tags=["assistive-tech"])
service = AssistiveTechnologyService()

@router.post("/voice-control/{user_id}")
async def enable_voice(user_id: str):
    return await service.enable_voice_control(user_id)

@router.post("/eye-tracking/{user_id}")
async def config_eye_tracking(user_id: str):
    return await service.configure_eye_tracking(user_id)

@router.post("/switch-access/{user_id}")
async def setup_switch(user_id: str, switch_type: str = "single"):
    return await service.setup_switch_access(user_id, switch_type)

@router.post("/haptic/{device_id}")
async def enable_haptic(device_id: str):
    return await service.enable_haptic_feedback(device_id)

@router.post("/magnifier/{user_id}")
async def integrate_magnifier(user_id: str):
    return await service.integrate_screen_magnifier(user_id)
