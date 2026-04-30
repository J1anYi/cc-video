from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime


class ContentAnalytics(Base):
    """Analytics data for content items (movies, series, episodes)."""
    __tablename__ = "content_analytics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), unique=True, nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="movie")

    # View metrics
    total_views: Mapped[int] = mapped_column(Integer, default=0)
    unique_viewers: Mapped[int] = mapped_column(Integer, default=0)
    total_watch_time_seconds: Mapped[int] = mapped_column(Integer, default=0)

    # Completion metrics
    avg_completion_pct: Mapped[float] = mapped_column(Float, default=0.0)
    engagement_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Trending metrics
    last_24h_views: Mapped[int] = mapped_column(Integer, default=0)
    previous_24h_views: Mapped[int] = mapped_column(Integer, default=0)
    velocity: Mapped[float] = mapped_column(Float, default=1.0)
    momentum: Mapped[float] = mapped_column(Float, default=0.0)
    trending_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Metadata
    last_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    content = relationship("Movie", backref="content_analytics", uselist=False)


class ContentEngagementHeatmap(Base):
    """Engagement heatmap data for content items."""
    __tablename__ = "content_engagement_heatmap"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    timestamp_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    # Engagement metrics at this timestamp
    engagement_pct: Mapped[float] = mapped_column(Float, default=0.0)

    # Event counts
    play_count: Mapped[int] = mapped_column(Integer, default=0)
    pause_count: Mapped[int] = mapped_column(Integer, default=0)
    seek_count: Mapped[int] = mapped_column(Integer, default=0)
    rewind_count: Mapped[int] = mapped_column(Integer, default=0)
    drop_count: Mapped[int] = mapped_column(Integer, default=0)

    # Relationship
    content = relationship("Movie", backref="heatmap_data")
