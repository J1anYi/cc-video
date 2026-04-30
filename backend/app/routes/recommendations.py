from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.recommendation import RecommendationsResponse
from app.services.recommendation import recommendation_service


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=RecommendationsResponse)
async def get_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> RecommendationsResponse:
    """
    Get personalized recommendations and continue watching items.
    Requires authentication.
    """
    recommendations = await recommendation_service.get_personalized_recommendations(
        db, current_user.id, limit=10
    )
    continue_watching = await recommendation_service.get_continue_watching(
        db, current_user.id, limit=10
    )

    return RecommendationsResponse(
        recommendations=recommendations,
        continue_watching=continue_watching,
    )
