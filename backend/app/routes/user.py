from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.movie import PublicationStatus
from app.schemas.movie import MovieResponse, MovieListResponse
from app.services.movie import movie_service
from app.services.video_file import video_file_service
from app.services.video_streaming import video_streaming_service


router = APIRouter(tags=["movies"])


@router.get("/movies", response_model=MovieListResponse)
async def list_movies(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """List all published movies. Requires authentication."""
    movies = await movie_service.get_published(db, skip, limit)
    return MovieListResponse(movies=movies, total=len(movies))


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
