from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.watch_history import WatchHistory
from app.models.movie import Movie


class HistoryService:
    async def get_user_history(self, db: AsyncSession, user_id: int) -> List[WatchHistory]:
        """Get user's watch history sorted by most recent first."""
        result = await db.execute(
            select(WatchHistory)
            .options(selectinload(WatchHistory.movie))
            .where(WatchHistory.user_id == user_id)
            .order_by(WatchHistory.last_watched_at.desc())
        )
        return list(result.scalars().all())

    async def update_history(
        self, db: AsyncSession, user_id: int, movie_id: int, progress: int
    ) -> WatchHistory:
        """Create or update watch history entry."""
        # Clamp progress to 0-100
        progress = max(0, min(100, progress))

        # Check for existing entry
        result = await db.execute(
            select(WatchHistory).where(
                and_(
                    WatchHistory.user_id == user_id,
                    WatchHistory.movie_id == movie_id
                )
            )
        )
        entry = result.scalar_one_or_none()

        if entry:
            # Update existing entry
            entry.progress = progress
            entry.last_watched_at = datetime.utcnow()
        else:
            # Create new entry
            entry = WatchHistory(
                user_id=user_id,
                movie_id=movie_id,
                progress=progress,
                last_watched_at=datetime.utcnow(),
            )
            db.add(entry)

        await db.commit()
        await db.refresh(entry)
        return entry

    async def get_history_entry(
        self, db: AsyncSession, user_id: int, movie_id: int
    ) -> Optional[WatchHistory]:
        """Get a single history entry for a specific movie."""
        result = await db.execute(
            select(WatchHistory)
            .options(selectinload(WatchHistory.movie))
            .where(
                and_(
                    WatchHistory.user_id == user_id,
                    WatchHistory.movie_id == movie_id
                )
            )
        )
        return result.scalar_one_or_none()


history_service = HistoryService()
