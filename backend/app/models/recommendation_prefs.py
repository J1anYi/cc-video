from sqlalchemy import Column, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class UserRecommendationPrefs(Base):
    """User recommendation preferences."""
    __tablename__ = "user_recommendation_prefs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    genre_weights = Column(JSON, default=dict)
    recency_weight = Column(Float, default=0.3)
    social_weight = Column(Float, default=0.3)
    popularity_weight = Column(Float, default=0.4)
    
    user = relationship("User", backref="rec_prefs")
