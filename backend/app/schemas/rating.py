from datetime import datetime
from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")


class RatingUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")


class RatingResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MovieRatingStats(BaseModel):
    average_rating: float | None = None
    rating_count: int = 0
    user_rating: int | None = None
