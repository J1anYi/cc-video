from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user, get_current_user_optional
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingResponse, MovieRatingStats
from app.services.rating import rating_service

router = APIRouter(prefix="/api", tags=["ratings"])

@router.post("/movies/{movie_id}/rating", response_model=RatingResponse)
async def set_rating(
    movie_id: int,
    rating_data: RatingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rating = await rating_service.create_or_update_rating(db, current_user.id, movie_id, rating_data)
    return rating

@router.get("/movies/{movie_id}/rating", response_model=MovieRatingStats)
async def get_movie_rating(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    user_id = current_user.id if current_user else None
    return await rating_service.get_movie_rating_stats(db, movie_id, user_id)

@router.delete("/movies/{movie_id}/rating")
async def delete_rating(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await rating_service.delete_rating(db, current_user.id, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"message": "Rating deleted"}

async def get_current_user_optional(current_user: User | None = Depends(get_current_user)):
    return current_user
