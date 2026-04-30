from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class UserAnalytics(Base):
    """Cached analytics data for users."""
    __tablename__ = "user_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Watch statistics
    total_watch_time_seconds = Column(Integer, default=0)
    total_movies_watched = Column(Integer, default=0)
    
    # Genre preferences (cached JSON)
    genre_breakdown = Column(JSON, default=dict)  # {"Action": 120, "Comedy": 45, ...}
    
    # Time patterns (cached JSON)
    hourly_pattern = Column(JSON, default=dict)  # {"0": 5, "1": 2, ..., "23": 10}
    daily_pattern = Column(JSON, default=dict)  # {"monday": 120, ...}
    
    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="analytics")
