from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.follow import (
    FollowResponse,
    FollowerResponse,
    FollowingResponse,
    FollowStatusResponse,
    FollowCountsResponse,
    UserBriefResponse,
)
from app.services.follow import follow_service


router = APIRouter(prefix="/api", tags=["follows"])


@router.post("/users/{user_id}/follow", response_model=FollowResponse)
async def follow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Follow a user."""
    try:
        follow = await follow_service.follow_user(db, current_user.id, user_id)
        return FollowResponse.model_validate(follow)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{user_id}/follow")
async def unfollow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Unfollow a user."""
    removed = await follow_service.unfollow_user(db, current_user.id, user_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Not following this user")
    return {"message": "Unfollowed successfully"}


@router.get("/users/{user_id}/followers", response_model=List[FollowerResponse])
async def get_followers(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
):
    """Get list of followers for a user."""
    follows = await follow_service.get_followers(db, user_id, skip, limit)
    return [
        FollowerResponse(
            id=f.id,
            follower=UserBriefResponse(
                id=f.follower.id,
                email=f.follower.email,
                display_name=f.follower.display_name,
            ),
            created_at=f.created_at,
        )
        for f in follows
    ]


@router.get("/users/{user_id}/following", response_model=List[FollowingResponse])
async def get_following(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
):
    """Get list of users that a user is following."""
    follows = await follow_service.get_following(db, user_id, skip, limit)
    return [
        FollowingResponse(
            id=f.id,
            following=UserBriefResponse(
                id=f.following.id,
                email=f.following.email,
                display_name=f.following.display_name,
            ),
            created_at=f.created_at,
        )
        for f in follows
    ]


@router.get("/users/{user_id}/follow/status", response_model=FollowStatusResponse)
async def get_follow_status(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if current user is following another user."""
    is_following = await follow_service.is_following(db, current_user.id, user_id)
    return FollowStatusResponse(is_following=is_following)


@router.get("/users/{user_id}/follow/counts", response_model=FollowCountsResponse)
async def get_follow_counts(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get follower and following counts for a user."""
    followers_count = await follow_service.get_followers_count(db, user_id)
    following_count = await follow_service.get_following_count(db, user_id)
    return FollowCountsResponse(
        followers_count=followers_count,
        following_count=following_count,
    )
