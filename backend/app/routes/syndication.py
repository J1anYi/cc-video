"""Content syndication routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import get_db
from app.auth import get_current_user
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.models.syndication import RSSFeed, ContentDistribution, ContentSchedule

router = APIRouter(prefix="/syndication", tags=["syndication"])

class FeedCreate(BaseModel):
    title: str
    feed_url: str

class DistributionCreate(BaseModel):
    movie_id: int
    platform: str

class ScheduleCreate(BaseModel):
    movie_id: int
    scheduled_for: str
    platforms: Optional[str] = None

@router.post("/feeds")
async def create_feed(data: FeedCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    feed = RSSFeed(tenant_id=tenant_id, title=data.title, feed_url=data.feed_url)
    db.add(feed)
    await db.commit()
    return {"id": feed.id, "title": feed.title}

@router.get("/feeds")
async def get_feeds(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    from sqlalchemy import select
    query = select(RSSFeed).where(RSSFeed.tenant_id == tenant_id, RSSFeed.is_active == True)
    result = await db.execute(query)
    feeds = result.scalars().all()
    return {"feeds": [{"id": f.id, "title": f.title, "feed_url": f.feed_url} for f in feeds]}

@router.post("/distribute")
async def create_distribution(data: DistributionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    dist = ContentDistribution(movie_id=data.movie_id, tenant_id=tenant_id, platform=data.platform)
    db.add(dist)
    await db.commit()
    return {"id": dist.id, "platform": dist.platform, "status": dist.status}

@router.post("/schedule")
async def create_schedule(data: ScheduleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    schedule = ContentSchedule(movie_id=data.movie_id, tenant_id=tenant_id, scheduled_for=datetime.fromisoformat(data.scheduled_for))
    db.add(schedule)
    await db.commit()
    return {"id": schedule.id, "scheduled_for": schedule.scheduled_for.isoformat(), "status": schedule.status}
