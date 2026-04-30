from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy import String, BigInteger, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.video_quality import VideoQuality
    from app.models.audio_track import AudioTrack

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
    hls_master_playlist: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    hls_segments_dir: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_hdr: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hdr_format: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    color_space: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    color_primaries: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    color_transfer: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    max_cll: Mapped[Optional[int]] = mapped_column(nullable=True)
    max_fall: Mapped[Optional[int]] = mapped_column(nullable=True)
    movie: Mapped["Movie"] = relationship("Movie", back_populates="video_files")
    quality_variants: Mapped[List["VideoQuality"]] = relationship("VideoQuality", back_populates="video_file")
    audio_tracks: Mapped[List["AudioTrack"]] = relationship("AudioTrack", back_populates="video_file")
