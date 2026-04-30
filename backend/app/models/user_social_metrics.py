from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, date


class UserSocialMetrics(Base):
    """Cached social metrics for users."""
    __tablename__ = "user_social_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Influence score
    influence_score = Column(Float, default=0)
    
    # Follower stats
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    
    # Review impact
    total_review_views = Column(Integer, default=0)
    total_helpful_votes = Column(Integer, default=0)
    review_count = Column(Integer, default=0)
    
    # Engagement
    avg_review_engagement = Column(Float, default=0)
    
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="social_metrics")


class FollowerHistory(Base):
    """Daily follower count history."""
    __tablename__ = "follower_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    follower_count = Column(Integer, default=0)
    
    user = relationship("User", backref="follower_history")
    
    class Config:
        unique_together = ('user_id', 'date')
