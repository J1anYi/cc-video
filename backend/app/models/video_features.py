from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VideoChapter(Base):
    __tablename__ = "video_chapters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_time: Mapped[int] = mapped_column(Integer, nullable=False)  # seconds
    end_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class SubtitleStyle(Base):
    __tablename__ = "subtitle_styles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    font_family: Mapped[str] = mapped_column(String(100), default="Arial")
    font_size: Mapped[int] = mapped_column(Integer, default=24)
    font_color: Mapped[str] = mapped_column(String(7), default="#FFFFFF")
    background_color: Mapped[str] = mapped_column(String(7), default="#000000")
    background_opacity: Mapped[float] = mapped_column(Float, default=0.5)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
