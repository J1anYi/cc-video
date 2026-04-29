from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

if TYPE_CHECKING:
    from app.models.video_file import VideoFile
    from app.models.subtitle import Subtitle


class PublicationStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DISABLED = "disabled"


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    poster_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    release_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    publication_status: Mapped[PublicationStatus] = mapped_column(
        SQLEnum(PublicationStatus), default=PublicationStatus.DRAFT, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to video files
    video_files: Mapped[list["VideoFile"]] = relationship("VideoFile", back_populates="movie")
    # Relationship to subtitles
    subtitles: Mapped[list["Subtitle"]] = relationship("Subtitle", back_populates="movie")
