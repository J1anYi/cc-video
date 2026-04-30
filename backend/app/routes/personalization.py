from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
import json

from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/personalization", tags=["personalization"])

class PersonalizationSettings(BaseModel):
    homepage_layout: Optional[dict] = None
    genre_weights: Optional[dict] = None
    mood_preferences: Optional[list] = None
    email_digest_enabled: bool = False
    email_digest_frequency: str = "weekly"

@router.get("/settings", response_model=PersonalizationSettings)
async def get_settings(current_user: User = Depends(get_current_user)):
    return PersonalizationSettings(
        homepage_layout=json.loads(current_user.homepage_layout) if current_user.homepage_layout else None,
        genre_weights=json.loads(current_user.genre_weights) if current_user.genre_weights else None,
        mood_preferences=json.loads(current_user.mood_preferences) if current_user.mood_preferences else None,
        email_digest_enabled=current_user.email_digest_enabled,
        email_digest_frequency=current_user.email_digest_frequency,
    )

@router.put("/genre-weights")
async def update_genre_weights(weights: dict[str, float], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.genre_weights = json.dumps(weights)
    await db.commit()
    return {"message": "Genre weights updated"}

@router.put("/homepage-layout")
async def update_layout(layout: list[dict], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.homepage_layout = json.dumps(layout)
    await db.commit()
    return {"message": "Layout updated"}

@router.put("/mood-preferences")
async def update_mood(moods: list[str], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.mood_preferences = json.dumps(moods)
    await db.commit()
    return {"message": "Mood preferences updated"}

@router.put("/email-digest")
async def update_email_digest(enabled: bool, frequency: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if frequency not in ["daily", "weekly", "monthly"]:
        raise HTTPException(status_code=400, detail="Invalid frequency")
    current_user.email_digest_enabled = enabled
    current_user.email_digest_frequency = frequency
    await db.commit()
    return {"message": "Email digest settings updated"}
