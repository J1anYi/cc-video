"""Gamification routes for achievements and rewards."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.gamification_service import GamificationService


router = APIRouter(prefix="/gamification", tags=["gamification"])
service = GamificationService()


class XPAdd(BaseModel):
    amount: int


class ChallengeProgress(BaseModel):
    progress: int


@router.get("/badges")
async def get_badges(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    badges = await service.get_badges(db, current_user.tenant_id)
    return [{"id": b.id, "name": b.name, "description": b.description, "icon": b.icon, "badge_type": b.badge_type.value, "xp_reward": b.xp_reward} for b in badges]


@router.get("/badges/my")
async def get_my_badges(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    badges = await service.get_user_badges(db, current_user.id)
    return [{"badge_id": b.badge_id, "earned_at": b.earned_at.isoformat()} for b in badges]


@router.get("/xp")
async def get_xp(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    xp = await service.get_user_xp(db, current_user.id)
    if not xp:
        return {"total_xp": 0, "level": 1}
    return {"total_xp": xp.total_xp, "level": xp.level}


@router.post("/xp")
async def add_xp(data: XPAdd, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    xp = await service.add_xp(db, current_user.id, current_user.tenant_id, data.amount)
    return {"total_xp": xp.total_xp, "level": xp.level}


@router.get("/leaderboard/{category}")
async def get_leaderboard(category: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = await service.get_leaderboard(db, current_user.tenant_id, category)
    return [{"user_id": e.user_id, "score": e.score, "rank": e.rank} for e in entries]


@router.get("/challenges")
async def get_challenges(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenges = await service.get_challenges(db, current_user.tenant_id)
    return [{"id": c.id, "title": c.title, "description": c.description, "xp_reward": c.xp_reward, "requirement_count": c.requirement_count} for c in challenges]


@router.get("/challenges/my")
async def get_my_challenges(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenges = await service.get_user_challenges(db, current_user.id)
    return [{"challenge_id": c.challenge_id, "progress": c.progress, "is_completed": c.is_completed} for c in challenges]


@router.post("/challenges/{challenge_id}/join")
async def join_challenge(challenge_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    uc = await service.join_challenge(db, current_user.id, challenge_id, current_user.tenant_id)
    if not uc:
        raise HTTPException(status_code=400, detail="Cannot join challenge")
    return {"message": "Challenge joined"}


@router.post("/challenges/{challenge_id}/progress")
async def update_progress(challenge_id: int, data: ChallengeProgress, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    uc = await service.update_challenge_progress(db, current_user.id, challenge_id, data.progress)
    if not uc:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return {"progress": uc.progress, "is_completed": uc.is_completed}


@router.get("/rewards")
async def get_rewards(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    rewards = await service.get_rewards(db, current_user.tenant_id)
    return [{"id": r.id, "name": r.name, "description": r.description, "level_required": r.level_required} for r in rewards]


@router.get("/rewards/my")
async def get_my_rewards(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    rewards = await service.get_user_rewards(db, current_user.id)
    return [{"reward_id": r.reward_id, "unlocked_at": r.unlocked_at.isoformat()} for r in rewards]


@router.post("/rewards/{reward_id}/unlock")
async def unlock_reward(reward_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    ur = await service.unlock_reward(db, current_user.id, reward_id, current_user.tenant_id)
    if not ur:
        raise HTTPException(status_code=400, detail="Cannot unlock reward")
    return {"message": "Reward unlocked"}
