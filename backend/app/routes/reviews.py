from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewListResponse
from app.services.review import review_service

router = APIRouter(prefix="/api", tags=["reviews"])

@router.post("/movies/{movie_id}/reviews", response_model=ReviewResponse)
async def create_review(
    movie_id: int,
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = await review_service.create_review(db, current_user.id, movie_id, review_data)
    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        movie_id=review.movie_id,
        username=current_user.display_name or current_user.email,
        content=review.content,
        created_at=review.created_at,
        updated_at=review.updated_at
    )

@router.get("/movies/{movie_id}/reviews", response_model=ReviewListResponse)
async def get_reviews(
    movie_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    reviews, total = await review_service.get_movie_reviews(db, movie_id, skip, limit)
    return ReviewListResponse(reviews=reviews, total=total)

@router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = await review_service.update_review(db, current_user.id, review_id, review_data)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        movie_id=review.movie_id,
        username=current_user.display_name or current_user.email,
        content=review.content,
        created_at=review.created_at,
        updated_at=review.updated_at
    )

@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await review_service.delete_review(db, current_user.id, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted"}
