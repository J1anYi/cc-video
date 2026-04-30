from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.watch_history import WatchHistory
from app.models.movie import Movie
from app.models.user_analytics import UserAnalytics
from app.models.viewing_session import ViewingSession
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json


class AnalyticsService:
    """Service for computing and caching user analytics."""
    
    @staticmethod
    async def get_or_create_analytics(db: AsyncSession, user_id: int) -> UserAnalytics:
        """Get existing analytics or create new record."""
        result = await db.execute(
            select(UserAnalytics).where(UserAnalytics.user_id == user_id)
        )
        analytics = result.scalar_one_or_none()
        
        if not analytics:
            analytics = UserAnalytics(user_id=user_id)
            db.add(analytics)
            await db.commit()
            await db.refresh(analytics)
        
        return analytics
    
    @staticmethod
    async def compute_watch_stats(db: AsyncSession, user_id: int) -> Dict[str, Any]:
        """Compute total watch time and movies watched from history."""
        # Get watch history with movie duration
        result = await db.execute(
            select(WatchHistory, Movie)
            .join(Movie, WatchHistory.movie_id == Movie.id)
            .where(WatchHistory.user_id == user_id)
        )
        rows = result.all()
        
        total_movies = len(set(row[0].movie_id for row in rows))
        total_seconds = sum(row[1].duration_minutes * 60 for row in rows if row[1].duration_minutes)
        
        return {
            "total_watch_time_seconds": total_seconds,
            "total_watch_time_hours": round(total_seconds / 3600, 1),
            "total_movies_watched": total_movies
        }
    
    @staticmethod
    async def compute_genre_breakdown(db: AsyncSession, user_id: int) -> Dict[str, int]:
        """Compute genre preferences from watch history."""
        result = await db.execute(
            select(Movie.genre, func.count(WatchHistory.id).label('count'))
            .join(WatchHistory, Movie.id == WatchHistory.movie_id)
            .where(WatchHistory.user_id == user_id)
            .where(Movie.genre.isnot(None))
            .group_by(Movie.genre)
            .order_by(func.count(WatchHistory.id).desc())
        )
        rows = result.all()
        
        return {row[0]: row[1] for row in rows if row[0]}
    
    @staticmethod
    async def compute_time_patterns(db: AsyncSession, user_id: int) -> Dict[str, Dict[str, int]]:
        """Compute viewing patterns by hour and day."""
        result = await db.execute(
            select(WatchHistory).where(WatchHistory.user_id == user_id)
        )
        histories = result.scalars().all()
        
        hourly = {str(h): 0 for h in range(24)}
        daily = {day: 0 for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']}
        
        for h in histories:
            if h.watched_at:
                hour = h.watched_at.hour
                day = h.watched_at.strftime('%A').lower()
                hourly[str(hour)] = hourly.get(str(hour), 0) + 1
                daily[day] = daily.get(day, 0) + 1
        
        return {
            "hourly": hourly,
            "daily": daily
        }
    
    @staticmethod
    async def refresh_analytics(db: AsyncSession, user_id: int) -> UserAnalytics:
        """Refresh cached analytics for a user."""
        analytics = await AnalyticsService.get_or_create_analytics(db, user_id)
        
        # Compute stats
        watch_stats = await AnalyticsService.compute_watch_stats(db, user_id)
        genre_breakdown = await AnalyticsService.compute_genre_breakdown(db, user_id)
        time_patterns = await AnalyticsService.compute_time_patterns(db, user_id)
        
        # Update analytics
        analytics.total_watch_time_seconds = watch_stats["total_watch_time_seconds"]
        analytics.total_movies_watched = watch_stats["total_movies_watched"]
        analytics.genre_breakdown = genre_breakdown
        analytics.hourly_pattern = time_patterns["hourly"]
        analytics.daily_pattern = time_patterns["daily"]
        analytics.last_updated = datetime.utcnow()
        
        await db.commit()
        await db.refresh(analytics)
        
        return analytics
    
    @staticmethod
    async def get_user_analytics(db: AsyncSession, user_id: int, force_refresh: bool = False) -> Dict[str, Any]:
        """Get analytics for a user, optionally forcing refresh."""
        analytics = await AnalyticsService.get_or_create_analytics(db, user_id)
        
        # Refresh if stale (older than 1 hour) or forced
        should_refresh = (
            force_refresh or 
            analytics.last_updated is None or
            (datetime.utcnow() - analytics.last_updated) > timedelta(hours=1)
        )
        
        if should_refresh:
            analytics = await AnalyticsService.refresh_analytics(db, user_id)
        
        return {
            "watch_time": {
                "total_hours": round(analytics.total_watch_time_seconds / 3600, 1),
                "total_movies": analytics.total_movies_watched
            },
            "genre_breakdown": analytics.genre_breakdown or {},
            "hourly_pattern": analytics.hourly_pattern or {},
            "daily_pattern": analytics.daily_pattern or {},
            "last_updated": analytics.last_updated.isoformat() if analytics.last_updated else None
        }
    
    @staticmethod
    async def get_activity_timeline(
        db: AsyncSession, 
        user_id: int, 
        activity_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> list:
        """Get recent activity timeline for a user."""
        from app.models.activity import Activity, ActivityType
        
        query = select(Activity).where(Activity.user_id == user_id)
        
        if activity_type:
            query = query.where(Activity.activity_type == activity_type)
        
        query = query.order_by(Activity.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        activities = result.scalars().all()
        
        return [
            {
                "id": a.id,
                "type": a.activity_type,
                "movie_id": a.movie_id,
                "created_at": a.created_at.isoformat()
            }
            for a in activities
        ]
    
    @staticmethod
    async def export_user_data(db: AsyncSession, user_id: int) -> Dict[str, Any]:
        """Export all user viewing data."""
        # Get watch history
        history_result = await db.execute(
            select(WatchHistory, Movie)
            .join(Movie, WatchHistory.movie_id == Movie.id)
            .where(WatchHistory.user_id == user_id)
            .order_by(WatchHistory.watched_at.desc())
        )
        history_rows = history_result.all()
        
        watch_history = [
            {
                "movie_title": row[1].title,
                "movie_id": row[0].movie_id,
                "watched_at": row[0].watched_at.isoformat() if row[0].watched_at else None,
                "completed": row[0].completed
            }
            for row in history_rows
        ]
        
        # Get analytics
        analytics = await AnalyticsService.get_user_analytics(db, user_id)
        
        return {
            "export_date": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "watch_history": watch_history,
            "analytics": analytics
        }


analytics_service = AnalyticsService()
