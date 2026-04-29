from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.movie import PublicationStatus


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None


class MovieCreate(MovieBase):
    publication_status: PublicationStatus = PublicationStatus.DRAFT


class MovieResponse(MovieBase):
    id: int
    publication_status: PublicationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
