from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.user_follow import UserFollow
from app.models.review import Review
from app.models.helpful_vote import HelpfulVote
from app.models.user_social_metrics import UserSocialMetrics, FollowerHistory
from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional


class SocialAnalyticsService:
    """Service for social analytics."""
    
    @staticmethod
    async def get_social_analytics(db: AsyncSession, user_id: int) -> Dict[str, Any]:
        """Get all social analytics for a user."""
        metrics = await SocialAnalyticsService._get_or_create_metrics(db, user_id)
        growth = await SocialAnalyticsService._get_follower_growth(db, user_id)
        reviews = await SocialAnalyticsService._get_review_performance(db, user_id)
        
        return {
            "influence_score": metrics.influence_score,
            "followers": metrics.follower_count,
            "following": metrics.following_count,
            "follower_growth": growth,
            "review_stats": {
                "total_views": metrics.total_review_views,
                "total_helpful_votes": metrics.total_helpful_votes,
                "review_count": metrics.review_count,
                "avg_engagement": metrics.avg_review_engagement
            },
            "top_reviews": reviews[:5]
        }
    
    @staticmethod
    async def _get_or_create_metrics(db: AsyncSession, user_id: int) -> UserSocialMetrics:
        result = await db.execute(
            select(UserSocialMetrics).where(UserSocialMetrics.user_id == user_id)
        )
        metrics = result.scalar_one_or_none()
        if not metrics:
            metrics = UserSocialMetrics(user_id=user_id)
            db.add(metrics)
            await db.commit()
            await db.refresh(metrics)
        return metrics
    
    @staticmethod
    async def refresh_metrics(db: AsyncSession, user_id: int) -> UserSocialMetrics:
        metrics = await SocialAnalyticsService._get_or_create_metrics(db, user_id)
        followers = await db.execute(
            select(func.count(UserFollow.id)).where(UserFollow.following_id == user_id)
        )
        metrics.follower_count = followers.scalar() or 0
        following = await db.execute(
            select(func.count(UserFollow.id)).where(UserFollow.follower_id == user_id)
        )
        metrics.following_count = following.scalar() or 0
        reviews = await db.execute(select(Review).where(Review.user_id == user_id))
        user_reviews = reviews.scalars().all()
        metrics.review_count = len(user_reviews)
        if user_reviews:
            review_ids = [r.id for r in user_reviews]
            helpful = await db.execute(
                select(func.count(HelpfulVote.id)).where(HelpfulVote.review_id.in_(review_ids))
            )
            metrics.total_helpful_votes = helpful.scalar() or 0
            metrics.avg_review_engagement = metrics.total_helpful_votes / metrics.review_count
        else:
            metrics.total_helpful_votes = 0
            metrics.avg_review_engagement = 0
        metrics.influence_score = (
            metrics.follower_count * 10 + 
            metrics.review_count * 5 + 
            metrics.total_helpful_votes * 20
        )
        await db.commit()
        await db.refresh(metrics)
        return metrics
    
    @staticmethod
    async def _get_follower_growth(db: AsyncSession, user_id: int) -> List[Dict]:
        thirty_days_ago = date.today() - timedelta(days=30)
        result = await db.execute(
            select(FollowerHistory)
            .where(FollowerHistory.user_id == user_id)
            .where(FollowerHistory.date >= thirty_days_ago)
            .order_by(FollowerHistory.date)
        )
        history = result.scalars().all()
        return [{"date": h.date.isoformat(), "count": h.follower_count} for h in history]
    
    @staticmethod
    async def _get_review_performance(db: AsyncSession, user_id: int) -> List[Dict]:
        result = await db.execute(
            select(Review, func.count(HelpfulVote.id).label('helpful_count'))
            .outerjoin(HelpfulVote, Review.id == HelpfulVote.review_id)
            .where(Review.user_id == user_id)
            .group_by(Review.id)
            .order_by(func.count(HelpfulVote.id).desc())
        )
        rows = result.all()
        return [
            {"review_id": row[0].id, "movie_id": row[0].movie_id, 
             "content": row[0].content[:100], "helpful_votes": row[1]}
            for row in rows
        ]
    
    @staticmethod
    async def compare_with_user(db: AsyncSession, user_id: int, other_user_id: int) -> Dict[str, Any]:
        my_metrics = await SocialAnalyticsService._get_or_create_metrics(db, user_id)
        other_metrics = await SocialAnalyticsService._get_or_create_metrics(db, other_user_id)
        return {
            "you": {"influence_score": my_metrics.influence_score, "followers": my_metrics.follower_count,
                    "reviews": my_metrics.review_count, "helpful_votes": my_metrics.total_helpful_votes},
            "friend": {"influence_score": other_metrics.influence_score, "followers": other_metrics.follower_count,
                       "reviews": other_metrics.review_count, "helpful_votes": other_metrics.total_helpful_votes}
        }


social_analytics_service = SocialAnalyticsService()
