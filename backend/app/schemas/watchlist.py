from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class WatchlistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: bool = False


class WatchlistUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: Optional[bool] = None


class WatchlistItemCreate(BaseModel):
    movie_id: int


class WatchlistItemBatchCreate(BaseModel):
    movie_ids: list[int]


class MovieInWatchlist(BaseModel):
    id: int
    title: str
    poster_url: Optional[str] = None
    position: int
    added_at: datetime

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    is_public: bool
    movie_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WatchlistDetailResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime
    movies: list[MovieInWatchlist]

    class Config:
        from_attributes = True


class WatchlistListResponse(BaseModel):
    watchlists: list[WatchlistResponse]
    total: int


class PublicWatchlistResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    user_name: Optional[str]
    movie_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class PublicWatchlistDetailResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    user_name: Optional[str]
    is_public: bool
    created_at: datetime
    movies: list[MovieInWatchlist]

    class Config:
        from_attributes = True
