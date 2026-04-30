from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.watch_history import WatchHistory
from app.models.movie import Movie
from app.models.user import User
from app.models.content_metrics import ContentMetrics, PlatformMetrics
from app.models.rating import Rating
from app.models.review import Review
from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional


class ContentMetricsService:
    """Service for computing content and platform metrics."""
    
    @staticmethod
    async def get_movie_metrics(db: AsyncSession, movie_id: int) -> Dict[str, Any]:
        """Get performance metrics for a specific movie."""
        result = await db.execute(
            select(WatchHistory).where(WatchHistory.movie_id == movie_id)
        )
        watches = result.scalars().all()
        
        total_views = len(watches)
        unique_viewers = len(set(w.user_id for w in watches))
        total_watch_time = sum(w.watch_duration or 0 for w in watches)
        completions = sum(1 for w in watches if w.completed and w.completed >= 90)
        
        rating_result = await db.execute(
            select(func.avg(Rating.rating), func.count(Rating.id))
            .where(Rating.movie_id == movie_id)
        )
        avg_rating, rating_count = rating_result.one()
        
        review_result = await db.execute(
            select(func.count(Review.id)).where(Review.movie_id == movie_id)
        )
        review_count = review_result.scalar() or 0
        
        return {
            "movie_id": movie_id,
            "total_views": total_views,
            "unique_viewers": unique_viewers,
            "total_watch_time_hours": round(total_watch_time / 3600, 1),
            "completion_rate": round(completions / total_views * 100, 1) if total_views > 0 else 0,
            "avg_rating": round(avg_rating, 1) if avg_rating else None,
            "rating_count": rating_count or 0,
            "review_count": review_count,
            "engagement_score": (total_views * 1) + (rating_count or 0) * 5 + review_count * 10
        }
    
    @staticmethod
    async def get_platform_overview(db: AsyncSession) -> Dict[str, Any]:
        """Get platform-wide metrics overview."""
        views_result = await db.execute(select(func.count(WatchHistory.id)))
        total_views = views_result.scalar() or 0
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_result = await db.execute(
            select(func.count(func.distinct(WatchHistory.user_id)))
            .where(WatchHistory.watched_at >= thirty_days_ago)
        )
        active_users = active_result.scalar() or 0
        
        users_result = await db.execute(select(func.count(User.id)))
        total_users = users_result.scalar() or 0
        
        movies_result = await db.execute(
            select(func.count(Movie.id)).where(Movie.status == 'published')
        )
        total_movies = movies_result.scalar() or 0
        
        watch_time_result = await db.execute(
            select(func.sum(WatchHistory.watch_duration))
        )
        total_watch_time = watch_time_result.scalar() or 0
        
        return {
            "total_views": total_views,
            "active_users": active_users,
            "total_users": total_users,
            "total_movies": total_movies,
            "total_watch_time_hours": round(total_watch_time / 3600, 1),
            "engagement_rate": round(active_users / total_users * 100, 1) if total_users > 0 else 0
        }
    
    @staticmethod
    async def get_trending_content(db: AsyncSession, period: str = "week", limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing content."""
        if period == "week":
            start_date = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            start_date = datetime.utcnow() - timedelta(days=30)
        else:
            start_date = None
        
        query = (
            select(Movie, func.count(WatchHistory.id).label('view_count'))
            .join(WatchHistory, Movie.id == WatchHistory.movie_id)
            .where(Movie.status == 'published')
        )
        
        if start_date:
            query = query.where(WatchHistory.watched_at >= start_date)
        
        query = query.group_by(Movie.id).order_by(desc('view_count')).limit(limit)
        
        result = await db.execute(query)
        rows = result.all()
        
        return [
            {"id": row[0].id, "title": row[0].title, "views": row[1], "genre": row[0].genre}
            for row in rows
        ]
    
    @staticmethod
    async def get_content_rankings(db: AsyncSession, sort_by: str = "views", genre: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get content rankings with various sort options."""
        view_subq = (
            select(WatchHistory.movie_id, func.count(WatchHistory.id).label('view_count'))
            .group_by(WatchHistory.movie_id)
            .subquery()
        )
        
        rating_subq = (
            select(Rating.movie_id, func.avg(Rating.rating).label('avg_rating'))
            .group_by(Rating.movie_id)
            .subquery()
        )
        
        query = (
            select(Movie, view_subq.c.view_count, rating_subq.c.avg_rating)
            .outerjoin(view_subq, Movie.id == view_subq.c.movie_id)
            .outerjoin(rating_subq, Movie.id == rating_subq.c.movie_id)
            .where(Movie.status == 'published')
        )
        
        if genre:
            query = query.where(Movie.genre == genre)
        
        if sort_by == "views":
            query = query.order_by(desc(view_subq.c.view_count))
        elif sort_by == "rating":
            query = query.order_by(desc(rating_subq.c.avg_rating))
        elif sort_by == "recent":
            query = query.order_by(desc(Movie.created_at))
        
        query = query.limit(limit)
        
        result = await db.execute(query)
        rows = result.all()
        
        return [
            {"id": row[0].id, "title": row[0].title, "genre": row[0].genre, "views": row[1] or 0, "avg_rating": round(row[2], 1) if row[2] else None, "release_year": row[0].release_year}
            for row in rows
        ]
    
    @staticmethod
    async def get_retention_metrics(db: AsyncSession) -> Dict[str, Any]:
        """Get user retention metrics."""
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        new_users_result = await db.execute(
            select(User).where(User.created_at >= thirty_days_ago)
        )
        new_users = new_users_result.scalars().all()
        
        if not new_users:
            return {"new_users_30d": 0, "returning_users": 0, "retention_rate": 0}
        
        new_user_ids = [u.id for u in new_users]
        
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        returning_result = await db.execute(
            select(func.count(func.distinct(WatchHistory.user_id)))
            .where(WatchHistory.user_id.in_(new_user_ids))
            .where(WatchHistory.watched_at >= seven_days_ago)
        )
        returning_users = returning_result.scalar() or 0
        
        return {
            "new_users_30d": len(new_users),
            "returning_users_7d": returning_users,
            "retention_rate": round(returning_users / len(new_users) * 100, 1)
        }


content_metrics_service = ContentMetricsService()
