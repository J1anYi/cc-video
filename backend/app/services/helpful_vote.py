from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.helpful_vote import HelpfulVote
from app.schemas.helpful_vote import HelpfulVoteResponse, HelpfulVoteToggleResponse

class HelpfulVoteService:
    @staticmethod
    async def toggle_vote(db: AsyncSession, user_id: int, review_id: int) -> HelpfulVoteToggleResponse:
        result = await db.execute(
            select(HelpfulVote).where(HelpfulVote.user_id == user_id, HelpfulVote.review_id == review_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            await db.delete(existing)
            await db.commit()
            count_result = await db.execute(select(func.count(HelpfulVote.id)).where(HelpfulVote.review_id == review_id))
            count = count_result.scalar() or 0
            return HelpfulVoteToggleResponse(review_id=review_id, helpful_count=count, voted=False)
        vote = HelpfulVote(user_id=user_id, review_id=review_id)
        db.add(vote)
        await db.commit()
        count_result = await db.execute(select(func.count(HelpfulVote.id)).where(HelpfulVote.review_id == review_id))
        count = count_result.scalar() or 0
        return HelpfulVoteToggleResponse(review_id=review_id, helpful_count=count, voted=True)

    @staticmethod
    async def get_vote_status(db: AsyncSession, review_id: int, user_id: int | None = None) -> HelpfulVoteResponse:
        count_result = await db.execute(select(func.count(HelpfulVote.id)).where(HelpfulVote.review_id == review_id))
        count = count_result.scalar() or 0
        user_voted = False
        if user_id:
            vote_result = await db.execute(
                select(HelpfulVote).where(HelpfulVote.user_id == user_id, HelpfulVote.review_id == review_id)
            )
            user_voted = vote_result.scalar_one_or_none() is not None
        return HelpfulVoteResponse(review_id=review_id, helpful_count=count, user_voted=user_voted)

helpful_vote_service = HelpfulVoteService()
