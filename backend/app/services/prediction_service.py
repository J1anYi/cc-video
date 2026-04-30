from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.predictions import ContentPrediction, DemandForecast, PricingSuggestion, ContentGap
from app.models.movie import Movie
from app.models.content_analytics import ContentAnalytics
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import random


class PredictionService:
    """Service for ML-powered predictions."""

    @staticmethod
    async def predict_content_success(db: AsyncSession, content_id: int) -> Dict[str, Any]:
        """Predict content success score."""
        # Get content
        result = await db.execute(select(Movie).where(Movie.id == content_id))
        movie = result.scalar_one_or_none()

        if not movie:
            return {"content_id": content_id, "title": "Unknown", "success_score": 0, "predicted_views": 0, "confidence": 0}

        # Get analytics if exists
        analytics_result = await db.execute(
            select(ContentAnalytics).where(ContentAnalytics.content_id == content_id)
        )
        analytics = analytics_result.scalar_one_or_none()

        # Simple scoring (would be ML in production)
        score = 50.0
        factors = {}

        if analytics:
            if analytics.engagement_score > 50:
                score += 20
                factors["high_engagement"] = True
            if analytics.avg_completion_pct > 70:
                score += 15
                factors["good_completion"] = True
            if analytics.trending_score > 5:
                score += 10
                factors["trending"] = True

        # Genre popularity bonus
        if movie.genre in ["Action", "Comedy", "Drama"]:
            score += 10
            factors["popular_genre"] = movie.genre

        score = min(100, score)
        predicted_views = int(score * 1000)
        confidence = 0.6 + (random.random() * 0.3)

        return {
            "content_id": content_id,
            "title": movie.title,
            "success_score": round(score, 2),
            "predicted_views": predicted_views,
            "confidence": round(confidence, 2),
            "factors": factors,
        }

    @staticmethod
    async def forecast_demand(db: AsyncSession, days: int = 30) -> Dict[str, Any]:
        """Forecast demand for the next N days."""
        forecasts = []
        base_views = 5000

        for i in range(days):
            date = datetime.utcnow() + timedelta(days=i)
            # Add day-of-week variation
            day_factor = 1.2 if date.weekday() in [4, 5, 6] else 1.0
            # Add some randomness
            noise = random.uniform(0.8, 1.2)

            predicted_views = int(base_views * day_factor * noise)
            predicted_hours = int(predicted_views * 1.5)
            confidence = 0.7 + random.random() * 0.2

            forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "predicted_views": predicted_views,
                "predicted_hours": predicted_hours,
                "confidence": round(confidence, 2),
            })

        return {
            "forecasts": forecasts,
            "total_predicted_views": sum(f["predicted_views"] for f in forecasts),
        }

    @staticmethod
    async def predict_ltv(db: AsyncSession, user_id: int) -> Dict[str, Any]:
        """Predict user lifetime value."""
        from app.models.user import User
        from app.models.subscription import Subscription, RevenuePerUser

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            return {"user_id": user_id, "predicted_ltv": 0, "confidence": 0}

        # Get existing revenue data
        revenue_result = await db.execute(
            select(RevenuePerUser).where(RevenuePerUser.user_id == user_id)
        )
        revenue = revenue_result.scalar_one_or_none()

        # Get subscription
        sub_result = await db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        subscription = sub_result.scalar_one_or_none()

        base_ltv = 50.0
        factors = {}

        if revenue:
            if revenue.total_revenue > 0:
                base_ltv = revenue.total_revenue * 1.5
                factors["historical_revenue"] = revenue.total_revenue
            if revenue.subscription_months > 6:
                base_ltv *= 1.3
                factors["long_subscriber"] = True

        if subscription and subscription.status == "active":
            base_ltv += subscription.monthly_price * 12
            factors["active_subscription"] = True

        confidence = 0.5 + random.random() * 0.3

        return {
            "user_id": user_id,
            "predicted_ltv": round(base_ltv, 2),
            "confidence": round(confidence, 2),
            "factors": factors,
        }

    @staticmethod
    async def suggest_pricing(db: AsyncSession) -> Dict[str, Any]:
        """Suggest optimal pricing for plans."""
        from app.models.subscription import Subscription

        # Get current pricing stats
        result = await db.execute(
            select(Subscription.plan, func.avg(Subscription.monthly_price), func.count(Subscription.id))
            .where(Subscription.status == "active")
            .group_by(Subscription.plan)
        )
        plan_stats = result.all()

        suggestions = []
        current_prices = {"basic": 9.99, "pro": 19.99, "premium": 29.99}

        for plan, avg_price, count in plan_stats:
            current = current_prices.get(plan, avg_price or 9.99)

            # Simple heuristic
            if count > 100:
                suggested = current * 1.1  # Increase if popular
                reasoning = "High demand suggests room for price increase"
            elif count < 20:
                suggested = current * 0.9  # Decrease if unpopular
                reasoning = "Low adoption suggests price may be too high"
            else:
                suggested = current
                reasoning = "Current price appears optimal"

            suggestions.append({
                "plan": plan,
                "current_price": round(current, 2),
                "suggested_price": round(suggested, 2),
                "expected_revenue_change": round((suggested - current) * count, 2),
                "reasoning": reasoning,
            })

        return {"suggestions": suggestions}

    @staticmethod
    async def analyze_content_gaps(db: AsyncSession) -> Dict[str, Any]:
        """Analyze content gaps by genre."""
        # Get genre distribution
        result = await db.execute(
            select(Movie.genre, func.count(Movie.id)).group_by(Movie.genre)
        )
        genre_counts = dict(result.all())

        # Demand scores (would come from user requests/searches in production)
        demand_scores = {
            "Action": 0.9, "Comedy": 0.85, "Drama": 0.8, "Horror": 0.75,
            "Sci-Fi": 0.88, "Romance": 0.7, "Documentary": 0.6, "Thriller": 0.82,
        }

        gaps = []
        for genre, demand in demand_scores.items():
            supply = min(1.0, genre_counts.get(genre, 0) / 100)
            gap = demand - supply

            recommendation = None
            if gap > 0.3:
                recommendation = f"High demand, low supply. Consider acquiring more {genre} content."
            elif gap < -0.2:
                recommendation = f"Oversupplied. May want to promote existing {genre} content."

            gaps.append({
                "genre": genre,
                "demand_score": round(demand, 2),
                "supply_score": round(supply, 2),
                "gap_score": round(gap, 2),
                "recommendation": recommendation,
            })

        # Sort by gap score descending
        gaps.sort(key=lambda x: x["gap_score"], reverse=True)

        return {"gaps": gaps}


prediction_service = PredictionService()
