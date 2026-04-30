from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContentDRM(Base):
    __tablename__ = "content_drm"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    
    drm_type: Mapped[str] = mapped_column(String(50), nullable=False)  # widevine, fairplay, playready
    license_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class GeoBlock(Base):
    __tablename__ = "geo_blocks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    is_allowed: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
