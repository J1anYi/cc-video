from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.services.user_block import user_block_service


class BlockStatusResponse(BaseModel):
    is_blocked: bool


class BlockedUserResponse(BaseModel):
    id: int
    display_name: str
    blocked_at: datetime

    model_config = {"from_attributes": True}


router = APIRouter(prefix="/users", tags=["blocks"])


@router.post("/{user_id}/block", response_model=BlockStatusResponse)
async def block_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Block a user."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
    
    try:
        await user_block_service.block_user(db, current_user.id, user_id)
    except Exception as e:
        # Already blocked - idempotent
        pass
    
    return BlockStatusResponse(is_blocked=True)


@router.delete("/{user_id}/block", response_model=BlockStatusResponse)
async def unblock_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unblock a user."""
    await user_block_service.unblock_user(db, current_user.id, user_id)
    return BlockStatusResponse(is_blocked=False)


@router.get("/{user_id}/block/status", response_model=BlockStatusResponse)
async def get_block_status(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if current user has blocked the specified user."""
    is_blocked = await user_block_service.is_blocked(db, current_user.id, user_id)
    return BlockStatusResponse(is_blocked=is_blocked)


@router.get("/blocked", response_model=List[BlockedUserResponse])
async def get_blocked_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of users blocked by current user."""
    blocked = await user_block_service.get_blocked_users(db, current_user.id)
    return [
        BlockedUserResponse(
            id=user.id,
            display_name=user.display_name or user.email,
            blocked_at=block.created_at
        )
        for block, user in blocked
    ]
