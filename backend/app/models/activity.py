from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class ActivityType(str, enum.Enum):
    REVIEW_POSTED = "review_posted"
    RATING_ADDED = "rating_added"


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    movie_id: Mapped[int | None] = mapped_column(ForeignKey("movies.id"), nullable=True, index=True)
    reference_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # ID of the related entity (review, rating)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User")
    movie: Mapped["Movie"] = relationship("Movie")

    __table_args__ = (
        Index("ix_activities_user_created", "user_id", "created_at"),
    )
