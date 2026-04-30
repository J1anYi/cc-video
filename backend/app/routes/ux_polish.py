from fastapi import APIRouter
from typing import Dict, Any
from app.services.ux_polish import ux_polish_service

router = APIRouter(prefix="/api/ux-polish", tags=["ux-polish"])

@router.post("/workspace/{tenant_id}")
async def improve_workspace(tenant_id: str) -> Dict[str, Any]:
    return await ux_polish_service.improve_workspace_switching(tenant_id)

@router.post("/video-controls/{player_id}")
async def enhance_video_controls(player_id: str) -> Dict[str, Any]:
    return await ux_polish_service.enhance_video_controls(player_id)

@router.post("/party-management/{room_id}")
async def improve_party(room_id: str) -> Dict[str, Any]:
    return await ux_polish_service.improve_party_management(room_id)

@router.post("/ai-interface/{tenant_id}")
async def refine_ai(tenant_id: str) -> Dict[str, Any]:
    return await ux_polish_service.refine_ai_interface(tenant_id)

@router.post("/admin-dashboard/{tenant_id}")
async def enhance_admin(tenant_id: str) -> Dict[str, Any]:
    return await ux_polish_service.enhance_admin_dashboard(tenant_id)
