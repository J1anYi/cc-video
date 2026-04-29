from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user, get_current_user_optional, get_current_user_optional
from app.models.user import User
from app.schemas.helpful_vote import HelpfulVoteResponse, HelpfulVoteToggleResponse
from app.services.helpful_vote import helpful_vote_service

router = APIRouter(prefix="/api", tags=["helpful-votes"])

@router.post("/reviews/{review_id}/helpful", response_model=HelpfulVoteToggleResponse)
async def toggle_helpful(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await helpful_vote_service.toggle_vote(db, current_user.id, review_id)

@router.get("/reviews/{review_id}/helpful", response_model=HelpfulVoteResponse)
async def get_helpful_status(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else None
    return await helpful_vote_service.get_vote_status(db, review_id, user_id)
