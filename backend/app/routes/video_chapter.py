"""Video chapter routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user, get_current_user_optional
from app.models.user import User
from app.services.video_chapter_service import VideoChapterService


router = APIRouter(prefix="/chapters", tags=["chapters"])


class ChapterCreate(BaseModel):
    movie_id: int
    title: str
    start_time: int
    end_time: Optional[int] = None
    thumbnail_path: Optional[str] = None
    order: int = 0


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    thumbnail_path: Optional[str] = None


class BookmarkCreate(BaseModel):
    movie_id: int
    timestamp: int
    note: Optional[str] = None


@router.post("")
async def create_chapter(
    data: ChapterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = VideoChapterService(db)
    chapter = await service.create_chapter(
        movie_id=data.movie_id,
        title=data.title,
        start_time=data.start_time,
        end_time=data.end_time,
        thumbnail_path=data.thumbnail_path,
        order=data.order,
    )
    return {"id": chapter.id, "title": chapter.title}


@router.get("/movie/{movie_id}")
async def get_movie_chapters(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = VideoChapterService(db)
    chapters = await service.get_chapters_for_movie(movie_id)
    return {
        "chapters": [
            {
                "id": c.id,
                "title": c.title,
                "start_time": c.start_time,
                "end_time": c.end_time,
                "thumbnail_path": c.thumbnail_path,
            }
            for c in chapters
        ]
    }


@router.put("/{chapter_id}")
async def update_chapter(
    chapter_id: int,
    data: ChapterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = VideoChapterService(db)
    chapter = await service.update_chapter(
        chapter_id=chapter_id,
        title=data.title,
        start_time=data.start_time,
        end_time=data.end_time,
        thumbnail_path=data.thumbnail_path,
    )
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"id": chapter.id}


@router.delete("/{chapter_id}")
async def delete_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = VideoChapterService(db)
    success = await service.delete_chapter(chapter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"message": "Chapter deleted"}


@router.post("/bookmarks")
async def create_bookmark(
    data: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = VideoChapterService(db)
    bookmark = await service.create_bookmark(
        user_id=current_user.id,
        movie_id=data.movie_id,
        timestamp=data.timestamp,
        note=data.note,
    )
    return {"id": bookmark.id, "timestamp": bookmark.timestamp}


@router.get("/bookmarks")
async def get_bookmarks(
    movie_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = VideoChapterService(db)
    bookmarks = await service.get_user_bookmarks(current_user.id, movie_id)
    return {
        "bookmarks": [
            {
                "id": b.id,
                "movie_id": b.movie_id,
                "timestamp": b.timestamp,
                "note": b.note,
            }
            for b in bookmarks
        ]
    }


@router.delete("/bookmarks/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = VideoChapterService(db)
    success = await service.delete_bookmark(bookmark_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark deleted"}
