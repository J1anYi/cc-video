from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.movie import Movie


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='uq_user_movie_favorite'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User")
    movie: Mapped["Movie"] = relationship("Movie")
