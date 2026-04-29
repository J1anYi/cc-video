from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentListResponse
from app.services.comment import comment_service

router = APIRouter(prefix="/api", tags=["comments"])

@router.post("/reviews/{review_id}/comments", response_model=CommentResponse)
async def create_comment(
    review_id: int,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = await comment_service.create_comment(db, current_user.id, review_id, comment_data)
    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        review_id=comment.review_id,
        username=current_user.display_name or current_user.email,
        content=comment.content,
        created_at=comment.created_at
    )

@router.get("/reviews/{review_id}/comments", response_model=CommentListResponse)
async def get_comments(
    review_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    comments, total = await comment_service.get_review_comments(db, review_id, skip, limit)
    return CommentListResponse(comments=comments, total=total)

@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await comment_service.delete_comment(db, current_user.id, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted"}
