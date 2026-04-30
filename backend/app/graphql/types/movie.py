import strawberry
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


@strawberry.type
class MovieType:
    id: int
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    genre: Optional[str] = None
    poster_url: Optional[str] = None
    video_url: Optional[str] = None
    average_rating: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


@strawberry.type
class MovieDetail:
    movie: MovieType
    ratings_count: int
    reviews_count: int


@strawberry.input
class MovieFilterInput:
    genre: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    min_rating: Optional[float] = None
    search: Optional[str] = None


@strawberry.input
class MovieCreateInput:
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    genre: Optional[str] = None
    poster_url: Optional[str] = None
    video_url: Optional[str] = None


@strawberry.input
class MovieUpdateInput:
    title: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    duration_minutes: Optional[int] = None
    genre: Optional[str] = None
    poster_url: Optional[str] = None
    video_url: Optional[str] = None
