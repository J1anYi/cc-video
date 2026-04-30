"""Video chapter service."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video_chapter import VideoChapter, UserBookmark


class VideoChapterService:
    """Service for video chapter operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chapter(
        self,
        movie_id: int,
        title: str,
        start_time: int,
        end_time: int = None,
        thumbnail_path: str = None,
        order: int = 0,
    ) -> VideoChapter:
        chapter = VideoChapter(
            movie_id=movie_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            thumbnail_path=thumbnail_path,
            order=order,
        )
        self.db.add(chapter)
        await self.db.commit()
        await self.db.refresh(chapter)
        return chapter

    async def get_chapters_for_movie(self, movie_id: int) -> List[VideoChapter]:
        query = select(VideoChapter).where(
            VideoChapter.movie_id == movie_id
        ).order_by(VideoChapter.start_time.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_chapter(self, chapter_id: int) -> Optional[VideoChapter]:
        return await self.db.get(VideoChapter, chapter_id)

    async def update_chapter(
        self,
        chapter_id: int,
        title: str = None,
        start_time: int = None,
        end_time: int = None,
        thumbnail_path: str = None,
    ) -> Optional[VideoChapter]:
        chapter = await self.db.get(VideoChapter, chapter_id)
        if chapter:
            if title is not None:
                chapter.title = title
            if start_time is not None:
                chapter.start_time = start_time
            if end_time is not None:
                chapter.end_time = end_time
            if thumbnail_path is not None:
                chapter.thumbnail_path = thumbnail_path
            await self.db.commit()
            await self.db.refresh(chapter)
        return chapter

    async def delete_chapter(self, chapter_id: int) -> bool:
        chapter = await self.db.get(VideoChapter, chapter_id)
        if chapter:
            await self.db.delete(chapter)
            await self.db.commit()
            return True
        return False

    async def create_bookmark(
        self,
        user_id: int,
        movie_id: int,
        timestamp: int,
        note: str = None,
    ) -> UserBookmark:
        bookmark = UserBookmark(
            user_id=user_id,
            movie_id=movie_id,
            timestamp=timestamp,
            note=note,
        )
        self.db.add(bookmark)
        await self.db.commit()
        await self.db.refresh(bookmark)
        return bookmark

    async def get_user_bookmarks(self, user_id: int, movie_id: int = None) -> List[UserBookmark]:
        query = select(UserBookmark).where(
            UserBookmark.user_id == user_id
        )
        if movie_id:
            query = query.where(UserBookmark.movie_id == movie_id)
        query = query.order_by(UserBookmark.timestamp.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_bookmark(self, bookmark_id: int) -> bool:
        bookmark = await self.db.get(UserBookmark, bookmark_id)
        if bookmark:
            await self.db.delete(bookmark)
            await self.db.commit()
            return True
        return False
