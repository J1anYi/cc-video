import strawberry
from typing import Optional
from datetime import datetime


@strawberry.type
class ReviewType:
    id: int
    user_id: int
    movie_id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None


@strawberry.input
class ReviewCreateInput:
    movie_id: int
    content: str


@strawberry.input
class ReviewUpdateInput:
    content: str
