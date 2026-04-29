from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import get_current_user, get_db
from app.models.movie import PublicationStatus
from app.models.user import User
from app.schemas.movie import MovieResponse, MovieListResponse
from app.schemas.subtitle import SubtitleResponse, SubtitleListResponse
from app.schemas.user import UserResponse, ProfileUpdate, PasswordChange
from app.services.movie import movie_service
from app.services.video_file import video_file_service
from app.services.video_streaming import video_streaming_service
from app.services.history import history_service
from app.services.favorite import favorite_service
from app.services.subtitle import subtitle_service
from app.services.auth import auth_service


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


class FavoriteResponse(BaseModel):
    id: int
    movie_id: int
    created_at: datetime
    movie: Optional[MovieResponse] = None

    class Config:
        from_attributes = True


class FavoriteStatusResponse(BaseModel):
    is_favorite: bool


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
    movies = await movie_service.get_published_filtered(
        db, search=q, category=category, skip=skip, limit=limit
    )
    return MovieListResponse(movies=movies, total=len(movies))


@router.get("/categories", response_model=List[str])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await movie_service.get_categories(db)


@router.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
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
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie or movie.publication_status != PublicationStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Movie not found")

    video_files = await video_file_service.get_by_movie(db, movie_id)
    if not video_files:
        raise HTTPException(status_code=404, detail="No video file found")

    return await video_streaming_service.stream(video_files[0])


@router.get("/movies/{movie_id}/subtitles", response_model=SubtitleListResponse)
async def get_movie_subtitles(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie or movie.publication_status != PublicationStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    subtitles = await subtitle_service.get_by_movie(db, movie_id)
    return SubtitleListResponse(subtitles=subtitles)


@router.get("/history", response_model=List[WatchHistoryResponse])
async def get_watch_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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


@router.get("/favorites", response_model=List[FavoriteResponse])
async def get_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorites = await favorite_service.get_user_favorites(db, current_user.id)
    return [
        FavoriteResponse(
            id=f.id,
            movie_id=f.movie_id,
            created_at=f.created_at,
            movie=MovieResponse.model_validate(f.movie) if f.movie else None
        )
        for f in favorites
    ]


@router.post("/favorites", response_model=FavoriteResponse)
async def add_favorite(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie or movie.publication_status != PublicationStatus.PUBLISHED:
        raise HTTPException(status_code=404, detail="Movie not found")

    favorite = await favorite_service.add_favorite(db, current_user.id, movie_id)
    return FavoriteResponse(
        id=favorite.id,
        movie_id=favorite.movie_id,
        created_at=favorite.created_at,
        movie=MovieResponse.model_validate(movie)
    )


@router.delete("/favorites/{movie_id}")
async def remove_favorite(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    removed = await favorite_service.remove_favorite(db, current_user.id, movie_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Removed from favorites"}


@router.get("/favorites/{movie_id}/status", response_model=FavoriteStatusResponse)
async def get_favorite_status(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    is_fav = await favorite_service.is_favorite(db, current_user.id, movie_id)
    return FavoriteStatusResponse(is_favorite=is_fav)


# Profile endpoints
@router.get("/users/me", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user's profile."""
    return UserResponse.model_validate(current_user)


@router.put("/users/me", response_model=UserResponse)
async def update_profile(
    data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Update current user's profile."""
    if data.display_name is not None:
        current_user.display_name = data.display_name
        current_user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.post("/users/me/password")
async def change_password(
    data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change current user's password."""
    # Verify current password
    if not auth_service.verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Update password
    current_user.hashed_password = auth_service.get_password_hash(data.new_password)
    current_user.updated_at = datetime.utcnow()
    await db.commit()

    return {"message": "Password changed successfully"}
