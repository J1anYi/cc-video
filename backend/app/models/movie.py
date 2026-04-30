from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, Integer, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.database import Base

if TYPE_CHECKING:
    from app.models.video_file import VideoFile
    from app.models.subtitle import Subtitle
    from app.models.video_chapter import VideoChapter, UserBookmark
    from app.models.tenant import Tenant

class PublicationStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DISABLED = "disabled"

class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        Index('ix_movies_category', 'category'),
        Index('ix_movies_created_at', 'created_at'),
        Index('ix_movies_publication_status', 'publication_status'),
        Index('ix_movies_language', 'language'),
        Index('ix_movies_tenant_id', 'tenant_id'),
    )
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    poster_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    release_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    original_language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    publication_status: Mapped[PublicationStatus] = mapped_column(SQLEnum(PublicationStatus), default=PublicationStatus.DRAFT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tenant: Mapped[Optional["Tenant"]] = relationship("Tenant")
    video_files: Mapped[List["VideoFile"]] = relationship("VideoFile", back_populates="movie")
    subtitles: Mapped[List["Subtitle"]] = relationship("Subtitle", back_populates="movie")
    chapters: Mapped[List["VideoChapter"]] = relationship("VideoChapter", back_populates="movie", order_by="VideoChapter.order")
    user_bookmarks: Mapped[List["UserBookmark"]] = relationship("UserBookmark", back_populates="movie")
    quality_variants: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    chapters_json: Mapped[str | None] = mapped_column(String(5000), nullable=True)
    audio_tracks: Mapped[str | None] = mapped_column(String(2000), nullable=True)
