from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.user import User

class VideoChapter(Base):
    __tablename__ = "video_chapters"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    start_time: Mapped[int] = mapped_column(Integer, nullable=False)  # seconds
    end_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    thumbnail_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    movie: Mapped["Movie"] = relationship("Movie", back_populates="chapters")

class UserBookmark(Base):
    __tablename__ = "user_bookmarks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)  # seconds
    note: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="user_bookmarks")
