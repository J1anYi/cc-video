from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.recommendation_prefs import UserRecommendationPrefs
from typing import Dict, Any, List


class RecInsightsService:
    @staticmethod
    async def get_prefs(db, user_id: int) -> UserRecommendationPrefs:
        result = await db.execute(
            select(UserRecommendationPrefs).where(UserRecommendationPrefs.user_id == user_id)
        )
        prefs = result.scalar_one_or_none()
        if not prefs:
            prefs = UserRecommendationPrefs(user_id=user_id)
            db.add(prefs)
            await db.commit()
            await db.refresh(prefs)
        return prefs
    
    @staticmethod
    async def update_prefs(db, user_id: int, data: Dict) -> UserRecommendationPrefs:
        prefs = await RecInsightsService.get_prefs(db, user_id)
        if "genre_weights" in data:
            prefs.genre_weights = data["genre_weights"]
        if "recency_weight" in data:
            prefs.recency_weight = data["recency_weight"]
        if "social_weight" in data:
            prefs.social_weight = data["social_weight"]
        if "popularity_weight" in data:
            prefs.popularity_weight = data["popularity_weight"]
        await db.commit()
        return prefs
    
    @staticmethod
    def explain_recommendation(movie, user_history=None, similar_users=None) -> Dict[str, Any]:
        reasons = []
        similarity_score = 0.5
        if user_history:
            reasons.append({"type": "watch_history", "desc": "Based on your watch history"})
        if similar_users:
            reasons.append({"type": "similar_users", "desc": "Popular with similar viewers"})
        reasons.append({"type": "genre_match", "desc": "Matches your genre preferences"})
        return {"reasons": reasons, "similarity_score": similarity_score}


rec_insights_service = RecInsightsService()
