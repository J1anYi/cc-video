from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

if TYPE_CHECKING:
    from app.models.video_file import VideoFile


class QualityLevel(str, enum.Enum):
    """Video quality levels for adaptive streaming."""
    QUALITY_4K = "4K"      # 3840x2160
    QUALITY_1080P = "1080p"  # 1920x1080
    QUALITY_720P = "720p"   # 1280x720
    QUALITY_480P = "480p"   # 854x480
    QUALITY_360P = "360p"   # 640x360


QUALITY_RESOLUTIONS = {
    QualityLevel.QUALITY_4K: (3840, 2160),
    QualityLevel.QUALITY_1080P: (1920, 1080),
    QualityLevel.QUALITY_720P: (1280, 720),
    QualityLevel.QUALITY_480P: (854, 480),
    QualityLevel.QUALITY_360P: (640, 360),
}

QUALITY_BITRATES = {
    QualityLevel.QUALITY_4K: 15000000,      # 15 Mbps
    QualityLevel.QUALITY_1080P: 5000000,    # 5 Mbps
    QualityLevel.QUALITY_720P: 2500000,     # 2.5 Mbps
    QualityLevel.QUALITY_480P: 1000000,     # 1 Mbps
    QualityLevel.QUALITY_360P: 600000,      # 600 Kbps
}


class VideoQuality(Base):
    """Video quality variant for adaptive streaming."""
    __tablename__ = "video_qualities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    video_file_id: Mapped[int] = mapped_column(ForeignKey("video_files.id"), nullable=False)
    quality: Mapped[QualityLevel] = mapped_column(SQLEnum(QualityLevel), nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    bitrate: Mapped[int] = mapped_column(Integer, nullable=False)  # bits per second
    playlist_path: Mapped[str] = mapped_column(String(500), nullable=False)  # Path to .m3u8 playlist
    segments_dir: Mapped[str] = mapped_column(String(500), nullable=False)  # Directory containing .ts segments
    file_size: Mapped[int] = mapped_column(Integer, default=0)  # Total size of all segments
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    video_file: Mapped["VideoFile"] = relationship("VideoFile", back_populates="quality_variants")

    @property
    def resolution(self) -> str:
        return f"{self.width}x{self.height}"
