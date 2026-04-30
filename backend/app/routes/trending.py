from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.trending import TrendingResponse, RelatedMoviesResponse
from app.services.trending import trending_service


router = APIRouter(tags=["trending"])


@router.get("/trending", response_model=TrendingResponse)
async def get_trending(
    db: AsyncSession = Depends(get_db),
) -> TrendingResponse:
    """Get trending movies (public, no auth required)."""
    movies = await trending_service.get_trending_movies(db, limit=10)
    return TrendingResponse(movies=movies)


@router.get("/movies/{movie_id}/related", response_model=RelatedMoviesResponse)
async def get_related(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
) -> RelatedMoviesResponse:
    """Get related movies by category (public, no auth required)."""
    movies = await trending_service.get_related_movies(db, movie_id, limit=4)
    return RelatedMoviesResponse(movies=movies)
