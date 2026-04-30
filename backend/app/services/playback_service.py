"""Playback settings service."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.playback import PlaybackSettings, WatchProgress


class PlaybackService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_settings(self, user_id: int) -> Optional[PlaybackSettings]:
        query = select(PlaybackSettings).where(PlaybackSettings.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_or_update_settings(
        self, user_id: int, tenant_id: int, default_speed: float = 1.0,
        auto_skip_intro: bool = True, auto_skip_credits: bool = False,
        auto_next_episode: bool = True, pip_enabled: bool = True,
        keyboard_shortcuts: dict = None,
    ) -> PlaybackSettings:
        settings = await self.get_settings(user_id)
        if settings:
            settings.default_speed = default_speed
            settings.auto_skip_intro = auto_skip_intro
            settings.auto_skip_credits = auto_skip_credits
            settings.auto_next_episode = auto_next_episode
            settings.pip_enabled = pip_enabled
            settings.keyboard_shortcuts = keyboard_shortcuts
        else:
            settings = PlaybackSettings(
                user_id=user_id, tenant_id=tenant_id, default_speed=default_speed,
                auto_skip_intro=auto_skip_intro, auto_skip_credits=auto_skip_credits,
                auto_next_episode=auto_next_episode, pip_enabled=pip_enabled,
                keyboard_shortcuts=keyboard_shortcuts,
            )
            self.db.add(settings)
        await self.db.commit()
        await self.db.refresh(settings)
        return settings

    async def save_progress(
        self, user_id: int, movie_id: int, tenant_id: int,
        position_seconds: int, duration_seconds: int,
    ) -> WatchProgress:
        query = select(WatchProgress).where(
            WatchProgress.user_id == user_id, WatchProgress.movie_id == movie_id,
        )
        result = await self.db.execute(query)
        progress = result.scalar_one_or_none()
        completion = (position_seconds / duration_seconds * 100) if duration_seconds > 0 else 0
        if progress:
            progress.position_seconds = position_seconds
            progress.duration_seconds = duration_seconds
            progress.completion_percentage = completion
        else:
            progress = WatchProgress(
                user_id=user_id, movie_id=movie_id, tenant_id=tenant_id,
                position_seconds=position_seconds, duration_seconds=duration_seconds,
                completion_percentage=completion,
            )
            self.db.add(progress)
        await self.db.commit()
        await self.db.refresh(progress)
        return progress

    async def get_progress(self, user_id: int, movie_id: int) -> Optional[WatchProgress]:
        query = select(WatchProgress).where(
            WatchProgress.user_id == user_id, WatchProgress.movie_id == movie_id,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_progress(self, user_id: int) -> List[WatchProgress]:
        query = select(WatchProgress).where(
            WatchProgress.user_id == user_id
        ).order_by(WatchProgress.last_played_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()
