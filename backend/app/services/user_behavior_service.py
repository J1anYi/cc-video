from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_journey import (
    UserJourneyEvent,
    UserSessionAnalytics,
    UserSegment,
    CohortAnalytics,
    ChurnRisk,
)
from app.models.user import User
from app.models.viewing_session import ViewingSession
from app.models.watch_history import WatchHistory
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List


class UserBehaviorService:
    """Service for user behavior analytics."""

    @staticmethod
    async def track_event(
        db: AsyncSession,
        user_id: int,
        session_id: str,
        event_type: str,
        event_data: Optional[Dict] = None,
        page_url: str = "",
        referrer_url: Optional[str] = None,
    ) -> UserJourneyEvent:
        """Log a journey event."""
        event = UserJourneyEvent(
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            event_data=event_data,
            page_url=page_url,
            referrer_url=referrer_url,
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

    @staticmethod
    async def get_user_journey(
        db: AsyncSession, user_id: int, limit: int = 100
    ) -> Dict[str, Any]:
        """Get user's recent journey events."""
        result = await db.execute(
            select(UserJourneyEvent)
            .where(UserJourneyEvent.user_id == user_id)
            .order_by(desc(UserJourneyEvent.created_at))
            .limit(limit)
        )
        events = result.scalars().all()

        return {
            "user_id": user_id,
            "events": [
                {
                    "id": e.id,
                    "user_id": e.user_id,
                    "event_type": e.event_type,
                    "event_data": e.event_data,
                    "page_url": e.page_url,
                    "referrer_url": e.referrer_url,
                    "created_at": e.created_at.isoformat(),
                }
                for e in events
            ],
            "total_events": len(events),
        }

    @staticmethod
    async def compute_session_metrics(
        db: AsyncSession, user_id: int
    ) -> Dict[str, Any]:
        """Compute session analytics for a user."""
        # Get viewing sessions
        result = await db.execute(
            select(ViewingSession)
            .where(ViewingSession.user_id == user_id)
            .order_by(ViewingSession.started_at)
        )
        sessions = result.scalars().all()

        if not sessions:
            return {
                "session_count": 0,
                "avg_session_duration_seconds": 0,
                "bounce_rate": 0.0,
                "peak_hour": 0,
            }

        # Calculate metrics
        durations = [s.duration_seconds or 0 for s in sessions]
        avg_duration = sum(durations) / len(durations) if durations else 0

        # Bounce rate: sessions < 30 seconds
        bounce_count = sum(1 for d in durations if d < 30)
        bounce_rate = (bounce_count / len(sessions)) * 100

        # Peak hour from session start times
        hour_counts = {}
        for s in sessions:
            if s.started_at:
                hour = s.started_at.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
        peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else 0

        return {
            "session_count": len(sessions),
            "avg_session_duration_seconds": int(avg_duration),
            "bounce_rate": round(bounce_rate, 2),
            "peak_hour": peak_hour,
        }

    @staticmethod
    async def get_session_metrics(
        db: AsyncSession, user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get session metrics for a user or aggregate."""
        if user_id:
            # Check for cached analytics
            result = await db.execute(
                select(UserSessionAnalytics).where(
                    UserSessionAnalytics.user_id == user_id
                )
            )
            analytics = result.scalar_one_or_none()

            if analytics:
                return {
                    "total_sessions": analytics.session_count,
                    "avg_duration_seconds": analytics.avg_session_duration_seconds,
                    "bounce_rate": analytics.bounce_rate,
                    "peak_hour": analytics.peak_hour,
                }

            # Compute fresh
            return await UserBehaviorService.compute_session_metrics(db, user_id)

        # Aggregate across all users
        result = await db.execute(select(func.count(ViewingSession.id)))
        total_sessions = result.scalar() or 0

        result = await db.execute(
            select(func.avg(ViewingSession.duration_seconds))
        )
        avg_duration = result.scalar() or 0

        return {
            "total_sessions": total_sessions,
            "avg_duration_seconds": int(avg_duration),
            "bounce_rate": 0.0,  # Would need more complex query
            "peak_hour": 0,
        }

    @staticmethod
    async def create_segment(
        db: AsyncSession,
        name: str,
        description: Optional[str],
        rules: List[Dict],
    ) -> UserSegment:
        """Create a new user segment."""
        segment = UserSegment(
            name=name,
            description=description,
            rules={"rules": rules},
        )
        db.add(segment)
        await db.commit()
        await db.refresh(segment)
        return segment

    @staticmethod
    async def get_segments(db: AsyncSession) -> List[Dict[str, Any]]:
        """List all segments."""
        result = await db.execute(select(UserSegment))
        segments = result.scalars().all()

        return [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "rules": s.rules.get("rules", []) if s.rules else [],
                "member_count": s.member_count,
                "created_at": s.created_at.isoformat(),
            }
            for s in segments
        ]

    @staticmethod
    async def get_cohort_analytics(
        db: AsyncSession, weeks: int = 12
    ) -> List[Dict[str, Any]]:
        """Get cohort retention analytics."""
        result = await db.execute(
            select(CohortAnalytics)
            .order_by(desc(CohortAnalytics.cohort_key))
            .limit(weeks)
        )
        cohorts = result.scalars().all()

        return [
            {
                "cohort_key": c.cohort_key,
                "signup_count": c.signup_count,
                "d1_retention": c.d1_retention,
                "d7_retention": c.d7_retention,
                "d14_retention": c.d14_retention,
                "d30_retention": c.d30_retention,
            }
            for c in cohorts
        ]

    @staticmethod
    async def calculate_all_cohorts(db: AsyncSession) -> None:
        """Calculate retention for all cohorts."""
        # Get users grouped by signup week
        result = await db.execute(select(User))
        users = result.scalars().all()

        # Group by week
        cohorts: Dict[str, List[User]] = {}
        for user in users:
            if user.created_at:
                week_key = user.created_at.strftime("%Y-W%W")
                if week_key not in cohorts:
                    cohorts[week_key] = []
                cohorts[week_key].append(user)

        # Calculate retention for each cohort
        for cohort_key, cohort_users in cohorts.items():
            signup_count = len(cohort_users)

            # Check for existing cohort record
            existing = await db.execute(
                select(CohortAnalytics).where(
                    CohortAnalytics.cohort_key == cohort_key
                )
            )
            cohort_record = existing.scalar_one_or_none()

            if not cohort_record:
                cohort_record = CohortAnalytics(
                    cohort_key=cohort_key, signup_count=signup_count
                )
                db.add(cohort_record)

            # Calculate retention at each interval
            now = datetime.utcnow()
            for days, attr in [(1, "d1_retention"), (7, "d7_retention"), (14, "d14_retention"), (30, "d30_retention")]:
                active_count = 0
                for user in cohort_users:
                    if user.last_login:
                        days_since_signup = (user.last_login - user.created_at).days
                        if days_since_signup >= days:
                            active_count += 1

                retention = (active_count / signup_count * 100) if signup_count > 0 else 0
                setattr(cohort_record, attr, round(retention, 2))

        await db.commit()

    @staticmethod
    async def calculate_churn_risk(
        db: AsyncSession, user_id: int
    ) -> Dict[str, Any]:
        """Calculate churn risk score for a user."""
        # Get user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            return {"risk_score": 0, "risk_factors": {}}

        score = 0.0
        factors = {}

        # Days since last login
        if user.last_login:
            days_since_login = (datetime.utcnow() - user.last_login).days
            if days_since_login > 14:
                score += 30
                factors["inactive_days"] = days_since_login
            elif days_since_login > 7:
                score += 15
                factors["inactive_days"] = days_since_login
        else:
            score += 40  # Never logged in
            factors["never_logged_in"] = True

        # Watch activity
        history_result = await db.execute(
            select(func.count(WatchHistory.id)).where(
                WatchHistory.user_id == user_id
            )
        )
        watch_count = history_result.scalar() or 0

        if watch_count < 3:
            score += 20
            factors["low_watch_count"] = watch_count

        # Session count
        session_result = await db.execute(
            select(func.count(ViewingSession.id)).where(
                ViewingSession.user_id == user_id
            )
        )
        session_count = session_result.scalar() or 0

        if session_count < 2:
            score += 15
            factors["low_session_count"] = session_count

        return {
            "risk_score": min(100, score),
            "risk_factors": factors,
        }

    @staticmethod
    async def get_at_risk_users(
        db: AsyncSession, threshold: float = 50.0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get users above churn risk threshold."""
        result = await db.execute(
            select(ChurnRisk, User)
            .join(User, ChurnRisk.user_id == User.id)
            .where(ChurnRisk.risk_score >= threshold)
            .order_by(desc(ChurnRisk.risk_score))
            .limit(limit)
        )
        rows = result.all()

        return [
            {
                "user_id": row[1].id,
                "email": row[1].email,
                "risk_score": row[0].risk_score,
                "risk_factors": row[0].risk_factors,
                "last_login_days": (
                    (datetime.utcnow() - row[1].last_login).days
                    if row[1].last_login
                    else None
                ),
            }
            for row in rows
        ]

    @staticmethod
    async def update_all_churn_risks(db: AsyncSession) -> None:
        """Update churn risk for all users."""
        result = await db.execute(select(User))
        users = result.scalars().all()

        for user in users:
            risk_data = await UserBehaviorService.calculate_churn_risk(db, user.id)

            # Check for existing record
            existing = await db.execute(
                select(ChurnRisk).where(ChurnRisk.user_id == user.id)
            )
            churn_record = existing.scalar_one_or_none()

            if not churn_record:
                churn_record = ChurnRisk(user_id=user.id)
                db.add(churn_record)

            churn_record.risk_score = risk_data["risk_score"]
            churn_record.risk_factors = risk_data["risk_factors"]
            churn_record.last_calculated = datetime.utcnow()

        await db.commit()


user_behavior_service = UserBehaviorService()
