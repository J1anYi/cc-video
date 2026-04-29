from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.movie import Movie
from app.models.report import Report, ReportStatus
from app.models.activity import Activity
from app.models.watch_history import WatchHistory
from datetime import datetime, timedelta
from typing import Dict, Any, List


class DashboardService:
    """Service for admin dashboard data."""
    
    @staticmethod
    async def get_dashboard_data(db: AsyncSession) -> Dict[str, Any]:
        """Get all dashboard data in single response."""
        # Get metrics
        metrics = await DashboardService._get_metrics(db)
        
        # Get recent activity
        activity = await DashboardService._get_recent_activity(db)
        
        # Get user growth
        growth = await DashboardService._get_user_growth(db)
        
        # Get content health
        health = await DashboardService._get_content_health(db)
        
        return {
            "metrics": metrics,
            "activity": activity,
            "growth": growth,
            "health": health
        }
    
    @staticmethod
    async def _get_metrics(db: AsyncSession) -> Dict[str, Any]:
        """Get key platform metrics."""
        # Total users
        total_users = await db.execute(select(func.count(User.id)))
        
        # New users today
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        new_today = await db.execute(
            select(func.count(User.id)).where(User.created_at >= today)
        )
        
        # Total movies
        total_movies = await db.execute(
            select(func.count(Movie.id)).where(Movie.status == 'published')
        )
        
        # Views today
        views_today = await db.execute(
            select(func.count(WatchHistory.id)).where(WatchHistory.watched_at >= today)
        )
        
        # Pending reports
        pending_reports = await db.execute(
            select(func.count(Report.id)).where(Report.status == ReportStatus.PENDING)
        )
        
        return {
            "total_users": total_users.scalar() or 0,
            "new_users_today": new_today.scalar() or 0,
            "total_movies": total_movies.scalar() or 0,
            "views_today": views_today.scalar() or 0,
            "pending_reports": pending_reports.scalar() or 0
        }
    
    @staticmethod
    async def _get_recent_activity(db: AsyncSession, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent platform activity."""
        result = await db.execute(
            select(Activity)
            .order_by(Activity.created_at.desc())
            .limit(limit)
        )
        activities = result.scalars().all()
        
        return [
            {
                "id": a.id,
                "type": a.activity_type,
                "user_id": a.user_id,
                "movie_id": a.movie_id,
                "created_at": a.created_at.isoformat()
            }
            for a in activities
        ]
    
    @staticmethod
    async def _get_user_growth(db: AsyncSession) -> Dict[str, Any]:
        """Get user growth trends."""
        # Daily growth for last 7 days
        daily = []
        for i in range(7):
            day_start = datetime.utcnow() - timedelta(days=6-i)
            day_start = day_start.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            count = await db.execute(
                select(func.count(User.id))
                .where(User.created_at >= day_start)
                .where(User.created_at < day_end)
            )
            daily.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "count": count.scalar() or 0
            })
        
        # Calculate growth rate
        if len(daily) >= 2:
            last_week = sum(d["count"] for d in daily[:3])
            this_week = sum(d["count"] for d in daily[4:])
            growth_rate = ((this_week - last_week) / last_week * 100) if last_week > 0 else 0
        else:
            growth_rate = 0
        
        return {
            "daily": daily,
            "growth_rate": round(growth_rate, 1)
        }
    
    @staticmethod
    async def _get_content_health(db: AsyncSession) -> Dict[str, Any]:
        """Get content health indicators."""
        # Pending reports
        pending_reports = await db.execute(
            select(func.count(Report.id)).where(Report.status == ReportStatus.PENDING)
        )
        
        # Stale content (no views in 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        stale_query = await db.execute(
            select(func.count(Movie.id))
            .where(Movie.status == 'published')
            .where(~Movie.id.in_(
                select(WatchHistory.movie_id)
                .where(WatchHistory.watched_at >= thirty_days_ago)
            ))
        )
        
        return {
            "pending_reports": pending_reports.scalar() or 0,
            "stale_content": stale_query.scalar() or 0
        }


dashboard_service = DashboardService()
