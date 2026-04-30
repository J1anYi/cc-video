"""Phase 191: Accessibility Routes"""
from fastapi import APIRouter
from ..services.accessibility_compliance import AccessibilityComplianceService

router = APIRouter(prefix="/api/accessibility", tags=["accessibility"])
service = AccessibilityComplianceService()

@router.post("/audit/{component}")
async def audit_wcag(component: str):
    return await service.audit_wcag_compliance(component)

@router.post("/screen-reader/{player_id}")
async def optimize_screen_reader(player_id: str):
    return await service.optimize_screen_reader(player_id)

@router.post("/keyboard/{component}")
async def enhance_keyboard(component: str):
    return await service.enhance_keyboard_navigation(component)

@router.get("/themes")
async def get_themes():
    return await service.create_accessibility_themes()

@router.post("/captions/{video_id}")
async def improve_captions(video_id: str):
    return await service.improve_caption_accessibility(video_id)
