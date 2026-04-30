from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.watch_history import WatchHistory
from app.models.viewing_session import ViewingSession
from app.models.movie import Movie
from app.models.content_analytics import ContentAnalytics, ContentEngagementHeatmap
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List


class ContentAnalyticsService:
    """Service for computing and caching content analytics."""

    @staticmethod
    async def get_or_create_analytics(db: AsyncSession, content_id: int) -> ContentAnalytics:
        """Get existing analytics or create new record."""
        result = await db.execute(
            select(ContentAnalytics).where(ContentAnalytics.content_id == content_id)
        )
        analytics = result.scalar_one_or_none()

        if not analytics:
            analytics = ContentAnalytics(content_id=content_id)
            db.add(analytics)
            await db.commit()
            await db.refresh(analytics)

        return analytics

    @staticmethod
    async def compute_content_metrics(db: AsyncSession, content_id: int) -> Dict[str, Any]:
        """Compute metrics for a content item from viewing sessions."""
        movie_result = await db.execute(select(Movie).where(Movie.id == content_id))
        movie = movie_result.scalar_one_or_none()
        duration_seconds = (movie.duration_minutes * 60) if movie and movie.duration_minutes else 0

        views_result = await db.execute(
            select(func.count(ViewingSession.id))
            .where(ViewingSession.movie_id == content_id)
        )
        total_views = views_result.scalar() or 0

        viewers_result = await db.execute(
            select(func.count(func.distinct(ViewingSession.user_id)))
            .where(ViewingSession.movie_id == content_id)
        )
        unique_viewers = viewers_result.scalar() or 0

        history_result = await db.execute(
            select(WatchHistory).where(WatchHistory.movie_id == content_id)
        )
        histories = history_result.scalars().all()

        if histories and duration_seconds > 0:
            completions = []
            for h in histories:
                if h.completed:
                    completions.append(100.0)
                elif h.watch_duration:
                    pct = min(100.0, (h.watch_duration / duration_seconds) * 100)
                    completions.append(pct)
            avg_completion = sum(completions) / len(completions) if completions else 0.0
        else:
            avg_completion = 0.0

        time_result = await db.execute(
            select(func.coalesce(func.sum(ViewingSession.duration_seconds), 0))
            .where(ViewingSession.movie_id == content_id)
        )
        total_watch_time = time_result.scalar() or 0

        engagement_score = 0.0
        if total_views > 0:
            completion_weight = avg_completion / 100.0
            engagement_score = round(
                (total_views * 0.3 + unique_viewers * 0.3 + completion_weight * 100 * 0.4), 2
            )

        return {
            "total_views": total_views,
            "unique_viewers": unique_viewers,
            "total_watch_time_seconds": total_watch_time,
            "avg_completion_pct": round(avg_completion, 2),
            "engagement_score": engagement_score,
        }

    @staticmethod
    async def refresh_content_analytics(db: AsyncSession, content_id: int) -> ContentAnalytics:
        analytics = await ContentAnalyticsService.get_or_create_analytics(db, content_id)
        metrics = await ContentAnalyticsService.compute_content_metrics(db, content_id)

        analytics.total_views = metrics["total_views"]
        analytics.unique_viewers = metrics["unique_viewers"]
        analytics.total_watch_time_seconds = metrics["total_watch_time_seconds"]
        analytics.avg_completion_pct = metrics["avg_completion_pct"]
        analytics.engagement_score = metrics["engagement_score"]
        analytics.last_updated = datetime.utcnow()

        await db.commit()
        await db.refresh(analytics)

        return analytics

    @staticmethod
    async def get_content_metrics(db: AsyncSession, content_id: int, force_refresh: bool = False) -> Dict[str, Any]:
        analytics = await ContentAnalyticsService.get_or_create_analytics(db, content_id)

        should_refresh = (
            force_refresh or
            analytics.last_updated is None or
            (datetime.utcnow() - analytics.last_updated) > timedelta(hours=1)
        )

        if should_refresh:
            analytics = await ContentAnalyticsService.refresh_content_analytics(db, content_id)

        movie_result = await db.execute(select(Movie).where(Movie.id == content_id))
        movie = movie_result.scalar_one_or_none()

        return {
            "content_id": content_id,
            "title": movie.title if movie else "Unknown",
            "total_views": analytics.total_views,
            "unique_viewers": analytics.unique_viewers,
            "avg_completion_pct": analytics.avg_completion_pct,
            "total_watch_time_hours": round(analytics.total_watch_time_seconds / 3600, 2),
            "engagement_score": analytics.engagement_score,
            "last_updated": analytics.last_updated.isoformat() if analytics.last_updated else None
        }

    @staticmethod
    async def get_engagement_heatmap(db: AsyncSession, content_id: int) -> Dict[str, Any]:
        movie_result = await db.execute(select(Movie).where(Movie.id == content_id))
        movie = movie_result.scalar_one_or_none()
        duration_seconds = (movie.duration_minutes * 60) if movie and movie.duration_minutes else 3600

        heatmap_result = await db.execute(
            select(ContentEngagementHeatmap)
            .where(ContentEngagementHeatmap.content_id == content_id)
            .order_by(ContentEngagementHeatmap.timestamp_seconds)
        )
        heatmap_data = heatmap_result.scalars().all()

        if not heatmap_data:
            samples = [
                {
                    "timestamp_seconds": i,
                    "engagement_pct": 100.0 - (i / duration_seconds * 30),
                    "play_count": 0,
                    "pause_count": 0,
                    "seek_count": 0,
                    "rewind_count": 0
                }
                for i in range(0, min(duration_seconds, 3600), 10)
            ]
        else:
            samples = [
                {
                    "timestamp_seconds": h.timestamp_seconds,
                    "engagement_pct": h.engagement_pct,
                    "play_count": h.play_count,
                    "pause_count": h.pause_count,
                    "seek_count": h.seek_count,
                    "rewind_count": h.rewind_count
                }
                for h in heatmap_data
            ]

        return {
            "content_id": content_id,
            "duration_seconds": duration_seconds,
            "samples": samples
        }

    @staticmethod
    async def compute_completion_analysis(db: AsyncSession, content_id: int) -> Dict[str, Any]:
        movie_result = await db.execute(select(Movie).where(Movie.id == content_id))
        movie = movie_result.scalar_one_or_none()
        duration_seconds = (movie.duration_minutes * 60) if movie and movie.duration_minutes else 3600

        history_result = await db.execute(
            select(WatchHistory).where(WatchHistory.movie_id == content_id)
        )
        histories = history_result.scalars().all()

        if not histories:
            return {
                "content_id": content_id,
                "completion_rate": 0.0,
                "avg_watch_duration_seconds": 0,
                "drop_off_points": []
            }

        completed_count = sum(1 for h in histories if h.completed)
        completion_rate = (completed_count / len(histories)) * 100 if histories else 0

        watch_durations = [h.watch_duration for h in histories if h.watch_duration]
        avg_watch_duration = int(sum(watch_durations) / len(watch_durations)) if watch_durations else 0

        drop_off_points = []
        if duration_seconds > 0 and watch_durations:
            for pct in range(10, 100, 10):
                timestamp = int(duration_seconds * pct / 100)
                viewers_at_point = sum(1 for d in watch_durations if d >= timestamp)
                drop_pct = ((len(watch_durations) - viewers_at_point) / len(watch_durations)) * 100
                drop_off_points.append({
                    "timestamp_seconds": timestamp,
                    "drop_pct": round(drop_pct, 2)
                })

        return {
            "content_id": content_id,
            "completion_rate": round(completion_rate, 2),
            "avg_watch_duration_seconds": avg_watch_duration,
            "drop_off_points": drop_off_points
        }

    @staticmethod
    async def compare_content(db: AsyncSession, content_ids: List[int]) -> List[Dict[str, Any]]:
        results = []
        for content_id in content_ids:
            metrics = await ContentAnalyticsService.get_content_metrics(db, content_id)
            results.append({
                "content_id": content_id,
                "title": metrics["title"],
                "total_views": metrics["total_views"],
                "unique_viewers": metrics["unique_viewers"],
                "avg_completion_pct": metrics["avg_completion_pct"],
                "engagement_score": metrics["engagement_score"]
            })
        return results

    @staticmethod
    async def get_trending_content(db: AsyncSession, limit: int = 20, time_range: str = "24h") -> List[Dict[str, Any]]:
        result = await db.execute(
            select(ContentAnalytics, Movie)
            .join(Movie, ContentAnalytics.content_id == Movie.id)
            .order_by(desc(ContentAnalytics.trending_score))
            .limit(limit)
        )
        rows = result.all()

        return [
            {
                "id": row[1].id,
                "title": row[1].title,
                "views_24h": row[0].last_24h_views,
                "velocity": row[0].velocity,
                "momentum": row[0].momentum,
                "trending_score": row[0].trending_score,
                "poster_url": row[1].poster_url
            }
            for row in rows
        ]

    @staticmethod
    async def update_trending_scores(db: AsyncSession) -> None:
        result = await db.execute(select(ContentAnalytics))
        analytics_list = result.scalars().all()

        for analytics in analytics_list:
            if analytics.previous_24h_views > 0:
                analytics.velocity = analytics.last_24h_views / analytics.previous_24h_views
            else:
                analytics.velocity = 1.0 if analytics.last_24h_views > 0 else 0.0

            analytics.momentum = (analytics.velocity - 1.0) * 0.5
            analytics.trending_score = round(
                analytics.velocity * 10 + analytics.momentum * 5 + analytics.engagement_score * 0.1, 2
            )

        await db.commit()


content_analytics_service = ContentAnalyticsService()
