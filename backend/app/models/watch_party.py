from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WatchParty(Base):
    __tablename__ = "watch_parties"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    current_time: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # seconds
    is_playing: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    host: Mapped["User"] = relationship("User")
    movie: Mapped["Movie"] = relationship("Movie")
    participants: Mapped[list["WatchPartyParticipant"]] = relationship(back_populates="party")


class WatchPartyParticipant(Base):
    __tablename__ = "watch_party_participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    party_id: Mapped[int] = mapped_column(ForeignKey("watch_parties.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    left_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    party: Mapped["WatchParty"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship("User")
