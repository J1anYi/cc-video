from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import get_current_user, get_db
from app.models.movie import PublicationStatus
from app.models.user import User
from app.schemas.movie import MovieResponse, MovieListResponse
from app.services.movie import movie_service
from app.services.video_file import video_file_service
from app.services.video_streaming import video_streaming_service
from app.services.history import history_service


class WatchHistoryUpdate(BaseModel):
    movie_id: int
    progress: int


class WatchHistoryResponse(BaseModel):
    id: int
    movie_id: int
    progress: int
    last_watched_at: datetime
    movie: Optional[MovieResponse] = None

    class Config:
        from_attributes = True


router = APIRouter(tags=["movies"])


@router.get("/movies", response_model=MovieListResponse)
async def list_movies(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    q: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """List published movies with optional search and category filter."""
    movies = await movie_service.get_published_filtered(
        db, search=q, category=category, skip=skip, limit=limit
    )
    return MovieListResponse(movies=movies, total=len(movies))


@router.get("/categories", response_model=List[str])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get list of available categories from published movies."""
    return await movie_service.get_categories(db)


@router.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get a single published movie by ID. Requires authentication."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie or movie.publication_status != PublicationStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.get("/movies/{movie_id}/stream")
async def stream_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Stream video file for a published movie. Requires authentication."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie or movie.publication_status != PublicationStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Movie not found")

    video_files = await video_file_service.get_by_movie(db, movie_id)
    if not video_files:
        raise HTTPException(status_code=404, detail="No video file found")

    return await video_streaming_service.stream(video_files[0])


# Watch History endpoints

@router.get("/history", response_model=List[WatchHistoryResponse])
async def get_watch_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's watch history sorted by most recent first."""
    history = await history_service.get_user_history(db, current_user.id)
    return [
        WatchHistoryResponse(
            id=h.id,
            movie_id=h.movie_id,
            progress=h.progress,
            last_watched_at=h.last_watched_at,
            movie=MovieResponse.model_validate(h.movie) if h.movie else None
        )
        for h in history
    ]


@router.post("/history", response_model=WatchHistoryResponse)
async def update_watch_history(
    data: WatchHistoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create or update watch history entry."""
    # Verify movie exists and is published
    movie = await movie_service.get_by_id(db, data.movie_id)
    if not movie or movie.publication_status != PublicationStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Movie not found")

    entry = await history_service.update_history(
        db, current_user.id, data.movie_id, data.progress
    )
    return WatchHistoryResponse(
        id=entry.id,
        movie_id=entry.movie_id,
        progress=entry.progress,
        last_watched_at=entry.last_watched_at,
        movie=MovieResponse.model_validate(movie)
    )


@router.get("/history/{movie_id}", response_model=WatchHistoryResponse)
async def get_history_entry(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get watch history entry for a specific movie."""
    entry = await history_service.get_history_entry(db, current_user.id, movie_id)
    if not entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    return WatchHistoryResponse(
        id=entry.id,
        movie_id=entry.movie_id,
        progress=entry.progress,
        last_watched_at=entry.last_watched_at,
        movie=MovieResponse.model_validate(entry.movie) if entry.movie else None
    )
