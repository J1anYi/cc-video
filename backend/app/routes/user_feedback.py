from fastapi import APIRouter
from typing import Dict, Any
from app.services.user_feedback import user_feedback_service

router = APIRouter(prefix="/api/feedback", tags=["user-feedback"])

@router.post("/widget/{tenant_id}")
async def create_widget(tenant_id: str) -> Dict[str, Any]:
    return await user_feedback_service.create_feedback_widget(tenant_id)

@router.post("/submit")
async def submit_feedback(user_id: str, feedback: str, category: str) -> Dict[str, Any]:
    return await user_feedback_service.submit_feedback(user_id, feedback, category)

@router.post("/feature-request")
async def create_feature_request(user_id: str, title: str, description: str) -> Dict[str, Any]:
    return await user_feedback_service.create_feature_request(user_id, title, description)

@router.post("/vote/{request_id}")
async def vote_feature(request_id: str, user_id: str) -> Dict[str, Any]:
    return await user_feedback_service.vote_feature(request_id, user_id)

@router.get("/categorize/{feedback_id}")
async def categorize_feedback(feedback_id: str) -> Dict[str, Any]:
    return await user_feedback_service.categorize_feedback(feedback_id)

@router.get("/roadmap/{tenant_id}")
async def get_roadmap(tenant_id: str) -> Dict[str, Any]:
    return await user_feedback_service.get_roadmap_transparency(tenant_id)

@router.get("/nps/{tenant_id}")
async def calculate_nps(tenant_id: str) -> Dict[str, Any]:
    return await user_feedback_service.calculate_nps(tenant_id)
