from datetime import datetime
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.activity import Activity, ActivityType
from app.models.user_follow import UserFollow


class ActivityService:
    async def create_activity(
        self,
        db: AsyncSession,
        user_id: int,
        activity_type: str,
        movie_id: int | None = None,
        reference_id: int | None = None,
    ) -> Activity:
        """Create a new activity."""
        activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            movie_id=movie_id,
            reference_id=reference_id,
            created_at=datetime.utcnow(),
        )
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        return activity

    async def get_feed(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Activity], int]:
        """Get activity feed from followed users."""
        # Get list of users that the current user follows
        following_result = await db.execute(
            select(UserFollow.following_id).where(UserFollow.follower_id == user_id)
        )
        following_ids = [row[0] for row in following_result.fetchall()]

        if not following_ids:
            return [], 0

        # Get activities from followed users
        result = await db.execute(
            select(Activity)
            .options(selectinload(Activity.user), selectinload(Activity.movie))
            .where(Activity.user_id.in_(following_ids))
            .order_by(Activity.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        activities = list(result.scalars().all())

        # Get total count
        count_result = await db.execute(
            select(Activity.id)
            .where(Activity.user_id.in_(following_ids))
        )
        total = len(count_result.fetchall())

        return activities, total

    async def get_user_activities(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Activity], int]:
        """Get activities for a specific user."""
        result = await db.execute(
            select(Activity)
            .options(selectinload(Activity.user), selectinload(Activity.movie))
            .where(Activity.user_id == user_id)
            .order_by(Activity.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        activities = list(result.scalars().all())

        # Get total count
        count_result = await db.execute(
            select(Activity.id).where(Activity.user_id == user_id)
        )
        total = len(count_result.fetchall())

        return activities, total


activity_service = ActivityService()
