import strawberry
from typing import Optional
from datetime import datetime


@strawberry.type
class RatingType:
    id: int
    user_id: int
    movie_id: int
    rating: float
    created_at: datetime
    updated_at: Optional[datetime] = None


@strawberry.input
class RatingCreateInput:
    movie_id: int
    rating: float


@strawberry.input
class RatingUpdateInput:
    rating: float
