"""Phase 195: Community Accessibility Routes"""
from fastapi import APIRouter
from ..services.community_accessibility import CommunityAccessibilityService

router = APIRouter(prefix="/api/community-accessibility", tags=["community-accessibility"])
service = CommunityAccessibilityService()

@router.post("/feedback-portal/{tenant_id}")
async def create_portal(tenant_id: str):
    return await service.create_feedback_portal(tenant_id)

@router.post("/captions/{video_id}")
async def enable_captions(video_id: str):
    return await service.enable_community_captions(video_id)

@router.post("/docs-center/{tenant_id}")
async def create_docs(tenant_id: str):
    return await service.create_documentation_center(tenant_id)

@router.post("/guidelines/{creator_id}")
async def publish_guidelines(creator_id: str):
    return await service.publish_design_guidelines(creator_id)

@router.post("/certification/{tenant_id}")
async def setup_certification(tenant_id: str):
    return await service.setup_certification_program(tenant_id)
