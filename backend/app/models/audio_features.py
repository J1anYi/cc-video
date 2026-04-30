from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AudioTrackFeature(Base):
    __tablename__ = "audio_track_features"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)

    language: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    is_default: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class AudioEqualizer(Base):
    __tablename__ = "audio_equalizers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    preset: Mapped[str] = mapped_column(String(50), default="custom")
    bands: Mapped[dict] = mapped_column(JSON, default=dict)
    
    is_active: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
