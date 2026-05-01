"""Music streaming schemas for Phase 226."""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Artist schemas
class ArtistBase(BaseModel):
    name: str = Field(..., max_length=255)
    bio: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)


class ArtistResponse(ArtistBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Album schemas
class AlbumBase(BaseModel):
    artist_id: str
    title: str = Field(..., max_length=255)
    release_date: Optional[date] = None
    cover_art_url: Optional[str] = Field(None, max_length=500)
    album_type: str = "album"


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    release_date: Optional[date] = None
    cover_art_url: Optional[str] = Field(None, max_length=500)
    album_type: Optional[str] = None


class AlbumResponse(AlbumBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Genre schemas
class GenreBase(BaseModel):
    name: str = Field(..., max_length=100)


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: str

    class Config:
        from_attributes = True


# Track schemas
class TrackBase(BaseModel):
    title: str = Field(..., max_length=255)
    album_id: Optional[str] = None
    duration_seconds: Optional[int] = None
    track_number: Optional[int] = None
    disc_number: int = 1


class TrackCreate(TrackBase):
    genre_ids: Optional[List[str]] = []


class TrackUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    album_id: Optional[str] = None
    duration_seconds: Optional[int] = None
    track_number: Optional[int] = None
    disc_number: Optional[int] = None
    genre_ids: Optional[List[str]] = []


class TrackResponse(TrackBase):
    id: str
    play_count: int
    created_at: datetime
    genres: List[GenreResponse] = []

    class Config:
        from_attributes = True


# Playback state schemas
class PlaybackStateUpdate(BaseModel):
    current_track_id: Optional[str] = None
    position_seconds: Optional[int] = None
    is_playing: Optional[bool] = None
    shuffle_mode: Optional[bool] = None
    repeat_mode: Optional[str] = None
    volume: Optional[float] = None


class PlaybackStateResponse(BaseModel):
    id: str
    user_id: str
    current_track_id: Optional[str] = None
    position_seconds: int
    is_playing: bool
    shuffle_mode: bool
    repeat_mode: str
    volume: float
    updated_at: datetime

    class Config:
        from_attributes = True
