from datetime import datetime
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    content: str = Field(..., min_length=10, max_length=2000, description="Review content")


class ReviewUpdate(BaseModel):
    content: str = Field(..., min_length=10, max_length=2000, description="Review content")


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    username: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    reviews: list[ReviewResponse]
    total: int
