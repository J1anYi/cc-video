from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie


class VideoFile(Base):
    __tablename__ = "video_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    movie: Mapped["Movie"] = relationship("Movie", back_populates="video_files")
