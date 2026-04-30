"""Social Feed service for personalized activity streams."""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social_feed import (
    SocialFeed, FeedPreference, TrendingDiscussion, FollowRecommendation, FeedItemType
)


class SocialFeedService:
    """Service for social feed operations."""
    
    async def get_feed(self, session: AsyncSession, user_id: int, tenant_id: int, limit: int = 50) -> List[SocialFeed]:
        result = await session.execute(
            select(SocialFeed).where(SocialFeed.user_id == user_id, SocialFeed.tenant_id == tenant_id)
            .order_by(desc(SocialFeed.created_at)).limit(limit)
        )
        return list(result.scalars().all())
    
    async def add_feed_item(self, session: AsyncSession, user_id: int, actor_id: int, tenant_id: int, item_type: FeedItemType, item_id: int, content: Optional[str] = None, movie_id: Optional[int] = None) -> SocialFeed:
        item = SocialFeed(user_id=user_id, actor_id=actor_id, tenant_id=tenant_id, item_type=item_type, item_id=item_id, content=content, movie_id=movie_id)
        session.add(item)
        await session.commit()
        return item
    
    async def mark_read(self, session: AsyncSession, feed_id: int) -> bool:
        result = await session.execute(select(SocialFeed).where(SocialFeed.id == feed_id))
        item = result.scalar_one_or_none()
        if not item:
            return False
        item.is_read = True
        await session.commit()
        return True
    
    async def mark_all_read(self, session: AsyncSession, user_id: int) -> int:
        result = await session.execute(select(SocialFeed).where(SocialFeed.user_id == user_id, SocialFeed.is_read == False))
        items = list(result.scalars().all())
        for item in items:
            item.is_read = True
        await session.commit()
        return len(items)
    
    async def get_preferences(self, session: AsyncSession, user_id: int) -> Optional[FeedPreference]:
        result = await session.execute(select(FeedPreference).where(FeedPreference.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def update_preferences(self, session: AsyncSession, user_id: int, tenant_id: int, **kwargs) -> FeedPreference:
        prefs = await self.get_preferences(session, user_id)
        if not prefs:
            prefs = FeedPreference(user_id=user_id, tenant_id=tenant_id)
            session.add(prefs)
        for key, value in kwargs.items():
            if hasattr(prefs, key) and value is not None:
                setattr(prefs, key, value)
        prefs.updated_at = datetime.utcnow()
        await session.commit()
        return prefs
    
    async def get_trending_discussions(self, session: AsyncSession, tenant_id: int, limit: int = 10) -> List[TrendingDiscussion]:
        result = await session.execute(
            select(TrendingDiscussion).where(TrendingDiscussion.tenant_id == tenant_id)
            .order_by(desc(TrendingDiscussion.score)).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_follow_recommendations(self, session: AsyncSession, user_id: int, limit: int = 10) -> List[FollowRecommendation]:
        result = await session.execute(
            select(FollowRecommendation).where(FollowRecommendation.user_id == user_id)
            .order_by(desc(FollowRecommendation.score)).limit(limit)
        )
        return list(result.scalars().all())
