from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class ViewingSession(Base):
    """Tracks individual viewing sessions for detailed analytics."""
    __tablename__ = "viewing_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    duration_seconds = Column(Integer, nullable=False)  # Time spent watching
    completed = Column(Integer, default=0)  # Percentage completed
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="viewing_sessions")
    movie = relationship("Movie")

    @property
    def duration_hours(self):
        return self.duration_seconds / 3600
