from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.rec_insights import rec_insights_service

router = APIRouter(prefix="/api", tags=["rec-insights"])


@router.get("/users/me/recommendation-preferences")
async def get_prefs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    prefs = await rec_insights_service.get_prefs(db, current_user.id)
    return {"genre_weights": prefs.genre_weights, "recency_weight": prefs.recency_weight,
            "social_weight": prefs.social_weight, "popularity_weight": prefs.popularity_weight}


@router.patch("/users/me/recommendation-preferences")
async def update_prefs(data: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    prefs = await rec_insights_service.update_prefs(db, current_user.id, data)
    return {"message": "Preferences updated", "preferences": {"genre_weights": prefs.genre_weights}}
