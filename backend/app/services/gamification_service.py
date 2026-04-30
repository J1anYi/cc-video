"""Gamification service for achievements and rewards."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gamification import (
    Badge, UserBadge, UserXP, Leaderboard, Challenge, UserChallenge, Reward, UserReward,
    BadgeType, AchievementType
)


class GamificationService:
    """Service for gamification operations."""
    
    async def get_badges(self, session: AsyncSession, tenant_id: int) -> List[Badge]:
        result = await session.execute(
            select(Badge).where(Badge.tenant_id == tenant_id, Badge.is_active == True)
        )
        return list(result.scalars().all())
    
    async def get_user_badges(self, session: AsyncSession, user_id: int) -> List[UserBadge]:
        result = await session.execute(
            select(UserBadge).where(UserBadge.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def award_badge(self, session: AsyncSession, user_id: int, badge_id: int, tenant_id: int) -> Optional[UserBadge]:
        existing = await session.execute(
            select(UserBadge).where(UserBadge.user_id == user_id, UserBadge.badge_id == badge_id)
        )
        if existing.scalar_one_or_none():
            return None
        badge = UserBadge(user_id=user_id, badge_id=badge_id, tenant_id=tenant_id)
        session.add(badge)
        badge_result = await session.execute(select(Badge).where(Badge.id == badge_id))
        badge_obj = badge_result.scalar_one_or_none()
        if badge_obj:
            await self.add_xp(session, user_id, tenant_id, badge_obj.xp_reward)
        await session.commit()
        return badge
    
    async def get_user_xp(self, session: AsyncSession, user_id: int) -> Optional[UserXP]:
        result = await session.execute(select(UserXP).where(UserXP.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def add_xp(self, session: AsyncSession, user_id: int, tenant_id: int, amount: int) -> UserXP:
        xp = await self.get_user_xp(session, user_id)
        if not xp:
            xp = UserXP(user_id=user_id, tenant_id=tenant_id)
            session.add(xp)
        xp.total_xp += amount
        xp.level = self._calculate_level(xp.total_xp)
        await session.commit()
        return xp
    
    def _calculate_level(self, total_xp: int) -> int:
        return int((total_xp / 100) ** 0.5) + 1
    
    async def get_leaderboard(self, session: AsyncSession, tenant_id: int, category: str, limit: int = 10) -> List[Leaderboard]:
        result = await session.execute(
            select(Leaderboard).where(
                Leaderboard.tenant_id == tenant_id,
                Leaderboard.category == category
            ).order_by(Leaderboard.rank).limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_challenges(self, session: AsyncSession, tenant_id: int) -> List[Challenge]:
        result = await session.execute(
            select(Challenge).where(Challenge.tenant_id == tenant_id, Challenge.is_active == True)
        )
        return list(result.scalars().all())
    
    async def get_user_challenges(self, session: AsyncSession, user_id: int) -> List[UserChallenge]:
        result = await session.execute(
            select(UserChallenge).where(UserChallenge.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def join_challenge(self, session: AsyncSession, user_id: int, challenge_id: int, tenant_id: int) -> Optional[UserChallenge]:
        existing = await session.execute(
            select(UserChallenge).where(UserChallenge.user_id == user_id, UserChallenge.challenge_id == challenge_id)
        )
        if existing.scalar_one_or_none():
            return None
        uc = UserChallenge(user_id=user_id, challenge_id=challenge_id, tenant_id=tenant_id)
        session.add(uc)
        await session.commit()
        return uc
    
    async def update_challenge_progress(self, session: AsyncSession, user_id: int, challenge_id: int, progress: int) -> Optional[UserChallenge]:
        result = await session.execute(
            select(UserChallenge).where(UserChallenge.user_id == user_id, UserChallenge.challenge_id == challenge_id)
        )
        uc = result.scalar_one_or_none()
        if not uc:
            return None
        uc.progress = progress
        challenge_result = await session.execute(select(Challenge).where(Challenge.id == challenge_id))
        challenge = challenge_result.scalar_one_or_none()
        if challenge and progress >= challenge.requirement_count and not uc.is_completed:
            uc.is_completed = True
            uc.completed_at = datetime.utcnow()
            await self.add_xp(session, user_id, uc.tenant_id, challenge.xp_reward)
        await session.commit()
        return uc
    
    async def get_rewards(self, session: AsyncSession, tenant_id: int) -> List[Reward]:
        result = await session.execute(
            select(Reward).where(Reward.tenant_id == tenant_id, Reward.is_active == True)
        )
        return list(result.scalars().all())
    
    async def get_user_rewards(self, session: AsyncSession, user_id: int) -> List[UserReward]:
        result = await session.execute(
            select(UserReward).where(UserReward.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def unlock_reward(self, session: AsyncSession, user_id: int, reward_id: int, tenant_id: int) -> Optional[UserReward]:
        existing = await session.execute(
            select(UserReward).where(UserReward.user_id == user_id, UserReward.reward_id == reward_id)
        )
        if existing.scalar_one_or_none():
            return None
        reward_result = await session.execute(select(Reward).where(Reward.id == reward_id))
        reward = reward_result.scalar_one_or_none()
        if not reward:
            return None
        xp = await self.get_user_xp(session, user_id)
        if not xp or xp.level < reward.level_required:
            return None
        ur = UserReward(user_id=user_id, reward_id=reward_id, tenant_id=tenant_id)
        session.add(ur)
        await session.commit()
        return ur
