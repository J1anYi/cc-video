from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.movie import PublicationStatus


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    language: str = "en"


class MovieCreate(MovieBase):
    original_language: Optional[str] = None
    publication_status: PublicationStatus = PublicationStatus.DRAFT


class MovieUpdate(BaseModel):
    """Schema for partial movie updates. All fields optional."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    language: Optional[str] = None
    original_language: Optional[str] = None
    publication_status: Optional[PublicationStatus] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    poster_path: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    language: str = "en"
    original_language: Optional[str] = None
    publication_status: PublicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MovieListResponse(BaseModel):
    """Schema for paginated movie list responses."""
    movies: List[MovieResponse]
    total: int
