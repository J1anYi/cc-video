from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.watchlist import Watchlist, WatchlistItem
from app.models.movie import Movie
from app.models.user import User
from app.models.activity import ActivityType
from app.services.activity import activity_service


class WatchlistService:
    async def get_user_watchlists(self, db: AsyncSession, user_id: int) -> List[Watchlist]:
        """Get user's watchlists with movie counts."""
        result = await db.execute(
            select(Watchlist)
            .where(Watchlist.user_id == user_id)
            .order_by(Watchlist.updated_at.desc())
        )
        return list(result.scalars().all())

    async def get_watchlist(self, db: AsyncSession, watchlist_id: int, user_id: int) -> Optional[Watchlist]:
        """Get a watchlist by ID (only if owned by user)."""
        result = await db.execute(
            select(Watchlist)
            .options(selectinload(Watchlist.items).selectinload(WatchlistItem.movie))
            .where(and_(Watchlist.id == watchlist_id, Watchlist.user_id == user_id))
        )
        return result.scalar_one_or_none()

    async def get_public_watchlist(self, db: AsyncSession, watchlist_id: int) -> Optional[Watchlist]:
        """Get a public watchlist by ID."""
        result = await db.execute(
            select(Watchlist)
            .options(selectinload(Watchlist.items).selectinload(WatchlistItem.movie), selectinload(Watchlist.user))
            .where(and_(Watchlist.id == watchlist_id, Watchlist.is_public == True))
        )
        return result.scalar_one_or_none()

    async def create_watchlist(
        self, db: AsyncSession, user_id: int, name: str, description: Optional[str], is_public: bool
    ) -> Watchlist:
        """Create a new watchlist."""
        watchlist = Watchlist(
            user_id=user_id,
            name=name,
            description=description,
            is_public=is_public,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(watchlist)
        await db.commit()
        await db.refresh(watchlist)

        # Create activity for watchlist creation
        await activity_service.create_activity(
            db, user_id, ActivityType.WATCHLIST_CREATED.value, reference_id=watchlist.id
        )

        return watchlist

    async def update_watchlist(
        self,
        db: AsyncSession,
        watchlist_id: int,
        user_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_public: Optional[bool] = None,
    ) -> Optional[Watchlist]:
        """Update a watchlist."""
        watchlist = await self.get_watchlist(db, watchlist_id, user_id)
        if not watchlist:
            return None

        if name is not None:
            watchlist.name = name
        if description is not None:
            watchlist.description = description
        if is_public is not None:
            watchlist.is_public = is_public
        watchlist.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(watchlist)
        return watchlist

    async def delete_watchlist(self, db: AsyncSession, watchlist_id: int, user_id: int) -> bool:
        """Delete a watchlist."""
        watchlist = await self.get_watchlist(db, watchlist_id, user_id)
        if not watchlist:
            return False

        await db.delete(watchlist)
        await db.commit()
        return True

    async def add_movie_to_watchlist(
        self, db: AsyncSession, watchlist_id: int, user_id: int, movie_id: int
    ) -> Optional[WatchlistItem]:
        """Add a movie to a watchlist."""
        watchlist = await self.get_watchlist(db, watchlist_id, user_id)
        if not watchlist:
            return None

        # Check if already exists
        existing = await self.get_watchlist_item(db, watchlist_id, movie_id)
        if existing:
            return existing

        # Get max position
        max_pos_result = await db.execute(
            select(func.max(WatchlistItem.position)).where(WatchlistItem.watchlist_id == watchlist_id)
        )
        max_pos = max_pos_result.scalar() or 0

        item = WatchlistItem(
            watchlist_id=watchlist_id,
            movie_id=movie_id,
            position=max_pos + 1,
            created_at=datetime.utcnow(),
        )
        db.add(item)

        # Update watchlist updated_at
        watchlist.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(item)
        return item

    async def remove_movie_from_watchlist(
        self, db: AsyncSession, watchlist_id: int, user_id: int, movie_id: int
    ) -> bool:
        """Remove a movie from a watchlist."""
        watchlist = await self.get_watchlist(db, watchlist_id, user_id)
        if not watchlist:
            return False

        item = await self.get_watchlist_item(db, watchlist_id, movie_id)
        if not item:
            return False

        await db.delete(item)
        watchlist.updated_at = datetime.utcnow()
        await db.commit()
        return True

    async def get_watchlist_item(
        self, db: AsyncSession, watchlist_id: int, movie_id: int
    ) -> Optional[WatchlistItem]:
        """Get a watchlist item."""
        result = await db.execute(
            select(WatchlistItem).where(
                and_(WatchlistItem.watchlist_id == watchlist_id, WatchlistItem.movie_id == movie_id)
            )
        )
        return result.scalar_one_or_none()

    async def get_movie_count(self, db: AsyncSession, watchlist_id: int) -> int:
        """Get movie count for a watchlist."""
        result = await db.execute(
            select(func.count(WatchlistItem.id)).where(WatchlistItem.watchlist_id == watchlist_id)
        )
        return result.scalar() or 0

    async def get_public_watchlists(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[Watchlist]:
        """Get all public watchlists."""
        result = await db.execute(
            select(Watchlist)
            .options(selectinload(Watchlist.user))
            .where(Watchlist.is_public == True)
            .order_by(Watchlist.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_user_public_watchlists(self, db: AsyncSession, user_id: int) -> List[Watchlist]:
        """Get a user's public watchlists."""
        result = await db.execute(
            select(Watchlist)
            .where(and_(Watchlist.user_id == user_id, Watchlist.is_public == True))
            .order_by(Watchlist.updated_at.desc())
        )
        return list(result.scalars().all())


watchlist_service = WatchlistService()
