from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum as SQLEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.database import Base

if TYPE_CHECKING:
    from app.models.video_file import VideoFile

class AudioChannelLayout(str, enum.Enum):
    STEREO = "stereo"
    SURROUND_5_1 = "5.1"
    SURROUND_7_1 = "7.1"

class AudioTrack(Base):
    __tablename__ = "audio_tracks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    video_file_id: Mapped[int] = mapped_column(ForeignKey("video_files.id"), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_original: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    channel_layout: Mapped[AudioChannelLayout] = mapped_column(SQLEnum(AudioChannelLayout), default=AudioChannelLayout.STEREO, nullable=False)
    codec: Mapped[str] = mapped_column(String(20), default="aac", nullable=False)
    bitrate: Mapped[int] = mapped_column(Integer, default=128000, nullable=False)
    sample_rate: Mapped[int] = mapped_column(Integer, default=48000, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    video_file: Mapped["VideoFile"] = relationship("VideoFile", back_populates="audio_tracks")
