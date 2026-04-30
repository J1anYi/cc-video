from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HelpfulVote(Base):
    __tablename__ = "helpful_votes"
    __table_args__ = (
        UniqueConstraint("user_id", "review_id", name="uq_user_review_helpful"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User")
    review: Mapped["Review"] = relationship("Review")
