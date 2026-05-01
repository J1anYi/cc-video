"""Music streaming routes for Phase 226."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.music import Artist, Album, Track, Genre
from app.schemas.music import (
    ArtistCreate, ArtistUpdate, ArtistResponse,
    AlbumCreate, AlbumUpdate, AlbumResponse,
    TrackCreate, TrackUpdate, TrackResponse,
    GenreCreate, GenreResponse, PlaybackStateUpdate, PlaybackStateResponse
)
from app.services.music_service import MusicService

router = APIRouter(prefix="/music", tags=["music"])


# Artist endpoints
@router.post("/artists", response_model=ArtistResponse)
async def create_artist(artist_data: ArtistCreate, db: AsyncSession = Depends(get_db)):
    return await MusicService.create_artist(db, artist_data.name, artist_data.bio, artist_data.image_url)


@router.get("/artists", response_model=list[ArtistResponse])
async def list_artists(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    return await MusicService.list_artists(db, skip, limit)


@router.get("/artists/{artist_id}", response_model=ArtistResponse)
async def get_artist(artist_id: str, db: AsyncSession = Depends(get_db)):
    artist = await MusicService.get_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.put("/artists/{artist_id}", response_model=ArtistResponse)
async def update_artist(artist_id: str, artist_data: ArtistUpdate, db: AsyncSession = Depends(get_db)):
    artist = await MusicService.get_artist(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    for key, value in artist_data.model_dump(exclude_unset=True).items():
        setattr(artist, key, value)
    await db.commit()
    await db.refresh(artist)
    return artist


@router.delete("/artists/{artist_id}")
async def delete_artist(artist_id: str, db: AsyncSession = Depends(get_db)):
    if not await MusicService.delete_artist(db, artist_id):
        raise HTTPException(status_code=404, detail="Artist not found")
    return {"message": "Artist deleted"}


# Album endpoints
@router.post("/albums", response_model=AlbumResponse)
async def create_album(album_data: AlbumCreate, db: AsyncSession = Depends(get_db)):
    return await MusicService.create_album(db, album_data.artist_id, album_data.title, album_data.release_date, album_data.cover_art_url, album_data.album_type)


@router.get("/albums", response_model=list[AlbumResponse])
async def list_albums(artist_id: Optional[str] = None, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    return await MusicService.list_albums(db, artist_id, skip, limit)


@router.get("/albums/{album_id}", response_model=AlbumResponse)
async def get_album(album_id: str, db: AsyncSession = Depends(get_db)):
    album = await MusicService.get_album(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.delete("/albums/{album_id}")
async def delete_album(album_id: str, db: AsyncSession = Depends(get_db)):
    if not await MusicService.delete_album(db, album_id):
        raise HTTPException(status_code=404, detail="Album not found")
    return {"message": "Album deleted"}


# Track endpoints
@router.post("/tracks", response_model=TrackResponse)
async def create_track(track_data: TrackCreate, db: AsyncSession = Depends(get_db)):
    return await MusicService.create_track(db, track_data.title, track_data.album_id, track_data.duration_seconds, track_data.track_number, track_data.disc_number, track_data.genre_ids)


@router.get("/tracks", response_model=list[TrackResponse])
async def list_tracks(album_id: Optional[str] = None, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    return await MusicService.list_tracks(db, album_id, skip, limit)


@router.get("/tracks/{track_id}", response_model=TrackResponse)
async def get_track(track_id: str, db: AsyncSession = Depends(get_db)):
    track = await MusicService.get_track(db, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.delete("/tracks/{track_id}")
async def delete_track(track_id: str, db: AsyncSession = Depends(get_db)):
    if not await MusicService.delete_track(db, track_id):
        raise HTTPException(status_code=404, detail="Track not found")
    return {"message": "Track deleted"}


# Genre endpoints
@router.post("/genres", response_model=GenreResponse)
async def create_genre(genre_data: GenreCreate, db: AsyncSession = Depends(get_db)):
    return await MusicService.create_genre(db, genre_data.name)


@router.get("/genres", response_model=list[GenreResponse])
async def list_genres(db: AsyncSession = Depends(get_db)):
    return await MusicService.list_genres(db)


# Search endpoint
@router.get("/search")
async def search_music(q: str, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50), db: AsyncSession = Depends(get_db)):
    return await MusicService.search_music(db, q, skip, limit)
