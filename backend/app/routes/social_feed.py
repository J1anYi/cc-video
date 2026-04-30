"""Social Feed routes for personalized activity streams."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.social_feed import FeedItemType
from app.services.social_feed_service import SocialFeedService


router = APIRouter(prefix="/social-feed", tags=["social-feed"])
service = SocialFeedService()


class PreferenceUpdate(BaseModel):
    show_reviews: Optional[bool] = None
    show_watchlist: Optional[bool] = None
    show_favorites: Optional[bool] = None
    show_discussions: Optional[bool] = None
    show_achievements: Optional[bool] = None


@router.get("")
async def get_feed(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = await service.get_feed(db, current_user.id, current_user.tenant_id)
    return [{"id": i.id, "actor_id": i.actor_id, "item_type": i.item_type.value, "item_id": i.item_id, "content": i.content, "movie_id": i.movie_id, "is_read": i.is_read, "created_at": i.created_at.isoformat()} for i in items]


@router.post("/{feed_id}/read")
async def mark_read(feed_id: int, db: AsyncSession = Depends(get_db)):
    if not await service.mark_read(db, feed_id):
        raise HTTPException(status_code=404, detail="Feed item not found")
    return {"message": "Marked as read"}


@router.post("/read-all")
async def mark_all_read(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    count = await service.mark_all_read(db, current_user.id)
    return {"marked_count": count}


@router.get("/preferences")
async def get_preferences(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    prefs = await service.get_preferences(db, current_user.id)
    if not prefs:
        return {"show_reviews": True, "show_watchlist": True, "show_favorites": True, "show_discussions": True, "show_achievements": True}
    return {"show_reviews": prefs.show_reviews, "show_watchlist": prefs.show_watchlist, "show_favorites": prefs.show_favorites, "show_discussions": prefs.show_discussions, "show_achievements": prefs.show_achievements}


@router.put("/preferences")
async def update_preferences(data: PreferenceUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    kwargs = {k: v for k, v in data.dict().items() if v is not None}
    prefs = await service.update_preferences(db, current_user.id, current_user.tenant_id, **kwargs)
    return {"message": "Preferences updated"}


@router.get("/trending")
async def get_trending(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = await service.get_trending_discussions(db, current_user.tenant_id)
    return [{"id": t.id, "discussion_type": t.discussion_type, "discussion_id": t.discussion_id, "score": t.score} for t in items]


@router.get("/recommendations")
async def get_recommendations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = await service.get_follow_recommendations(db, current_user.id)
    return [{"recommended_user_id": r.recommended_user_id, "reason": r.reason, "score": r.score} for r in items]
