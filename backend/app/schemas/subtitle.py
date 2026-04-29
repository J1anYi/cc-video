from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class SubtitleBase(BaseModel):
    language: str


class SubtitleCreate(SubtitleBase):
    """Schema for creating a subtitle."""


class SubtitleResponse(BaseModel):
    id: int
    movie_id: int
    language: str
    file_path: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SubtitleListResponse(BaseModel):
    """Schema for list of subtitles."""
    subtitles: List[SubtitleResponse]
