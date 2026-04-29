from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.movie import PublicationStatus


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None


class MovieCreate(MovieBase):
    publication_status: PublicationStatus = PublicationStatus.DRAFT


class MovieUpdate(BaseModel):
    """Schema for partial movie updates. All fields optional."""
    title: Optional[str] = None
    description: Optional[str] = None
    publication_status: Optional[PublicationStatus] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    publication_status: PublicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MovieListResponse(BaseModel):
    """Schema for paginated movie list responses."""
    movies: List[MovieResponse]
    total: int
