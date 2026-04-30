from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum as SQLEnum, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.database import Base

if TYPE_CHECKING:
    from app.models.video_file import VideoFile

class TranscodingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TranscodingJob(Base):
    __tablename__ = "transcoding_jobs"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    video_file_id: Mapped[int] = mapped_column(ForeignKey("video_files.id"), nullable=False)
    status: Mapped[TranscodingStatus] = mapped_column(SQLEnum(TranscodingStatus), default=TranscodingStatus.PENDING, nullable=False)
    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    current_task: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    preset: Mapped[str] = mapped_column(String(50), default="medium", nullable=False)
    hardware_accel: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    video_file: Mapped["VideoFile"] = relationship("VideoFile", back_populates="transcoding_jobs")
