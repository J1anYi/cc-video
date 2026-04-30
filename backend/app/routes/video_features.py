from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.video_features import VideoChapterFeature as VideoChapter, SubtitleStyle

router = APIRouter(prefix="/video-features", tags=["video-features"])


class ChapterCreate(BaseModel):
    movie_id: int
    title: str
    start_time: int
    end_time: int = None


class SubtitleStyleUpdate(BaseModel):
    font_family: str = "Arial"
    font_size: int = 24
    font_color: str = "#FFFFFF"


@router.post("/chapters")
async def create_chapter(data: ChapterCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    chapter = VideoChapter(movie_id=data.movie_id, title=data.title, start_time=data.start_time, end_time=data.end_time)
    db.add(chapter)
    await db.commit()
    return {"id": chapter.id, "title": chapter.title}


@router.get("/chapters/{movie_id}")
async def get_chapters(movie_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    query = select(VideoChapter).where(VideoChapter.movie_id == movie_id)
    result = await db.execute(query)
    chapters = result.scalars().all()
    return {"chapters": [{"id": c.id, "title": c.title, "start_time": c.start_time} for c in chapters]}


@router.put("/subtitle-style")
async def update_subtitle_style(data: SubtitleStyleUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    style = SubtitleStyle(user_id=current_user.id, font_family=data.font_family, font_size=data.font_size, font_color=data.font_color)
    db.add(style)
    await db.commit()
    return {"message": "Subtitle style updated"}
