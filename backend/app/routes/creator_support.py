"""Phase 200: Creator Support Routes"""
from fastapi import APIRouter
from ..services.creator_support import CreatorSupportService

router = APIRouter(prefix="/api/creator-support", tags=["creator-support"])
service = CreatorSupportService()

@router.get("/academy/{creator_id}")
async def access_academy(creator_id: str, course_id: str = None):
    return await service.access_academy(creator_id, course_id)

@router.post("/ticket/{creator_id}")
async def create_ticket(creator_id: str, ticket: dict):
    return await service.create_support_ticket(creator_id, ticket)

@router.get("/growth-tools/{creator_id}")
async def get_growth(creator_id: str):
    return await service.get_growth_tools(creator_id)

@router.post("/funding/{creator_id}")
async def apply_fund(creator_id: str, program: str):
    return await service.apply_funding(creator_id, program)

@router.post("/verification/{creator_id}")
async def request_verify(creator_id: str, reason: str):
    return await service.request_verification(creator_id, reason)
