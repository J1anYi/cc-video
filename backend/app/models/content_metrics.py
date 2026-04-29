from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, date


class ContentMetrics(Base):
    """Daily metrics for individual movies."""
    __tablename__ = "content_metrics"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Engagement metrics
    total_views = Column(Integer, default=0)
    unique_viewers = Column(Integer, default=0)
    total_watch_time_seconds = Column(Integer, default=0)
    completions = Column(Integer, default=0)  # Full watches
    
    # Computed metrics
    avg_watch_time_seconds = Column(Float, default=0)
    completion_rate = Column(Float, default=0)  # percentage
    
    # Engagement score (weighted combination)
    engagement_score = Column(Float, default=0)
    
    movie = relationship("Movie", backref="metrics")
    
    class Config:
        unique_together = ('movie_id', 'date')


class PlatformMetrics(Base):
    """Daily aggregated platform metrics."""
    __tablename__ = "platform_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False)
    
    # Platform-wide stats
    total_views = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    total_watch_time_hours = Column(Float, default=0)
    
    # Engagement
    avg_session_duration_minutes = Column(Float, default=0)
    
    # Content
    movies_added = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
