from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel

from app.schemas.movie import MovieResponse


class RecommendedMovie(BaseModel):
    """A movie recommendation with reason."""
    movie: MovieResponse
    reason: str  # e.g., "Because you watched Action movies"


class ContinueWatchingItem(BaseModel):
    """A movie the user hasn't finished watching."""
    movie: MovieResponse
    progress: int  # 0-100 percentage
    last_watched_at: str  # ISO datetime


class RecommendationsResponse(BaseModel):
    """Response containing both recommendation types."""
    recommendations: List[RecommendedMovie]
    continue_watching: List[ContinueWatchingItem]
