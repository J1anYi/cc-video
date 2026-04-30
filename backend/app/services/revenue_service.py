from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import Subscription, PaymentTransaction, RevenueAnalytics, RevenuePerUser
from app.models.user import User
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List


class RevenueService:
    """Service for revenue analytics."""

    @staticmethod
    async def get_revenue_trends(db: AsyncSession, period_type: str = "monthly", periods: int = 12) -> Dict[str, Any]:
        """Get revenue trends over time."""
        result = await db.execute(
            select(RevenueAnalytics)
            .where(RevenueAnalytics.period_type == period_type)
            .order_by(RevenueAnalytics.period_key.desc())
            .limit(periods)
        )
        analytics = result.scalars().all()
        return {
            "period_type": period_type,
            "data": [
                {
                    "period": a.period_key,
                    "total_revenue": a.total_revenue,
                    "new_revenue": a.new_revenue,
                    "churned_revenue": a.churned_revenue,
                    "net_revenue": a.net_revenue,
                }
                for a in reversed(analytics)
            ],
        }

    @staticmethod
    async def get_subscription_metrics(db: AsyncSession) -> Dict[str, Any]:
        """Get MRR, ARR, growth rate, churn rate."""
        # Count active subscriptions
        active_result = await db.execute(
            select(func.count(Subscription.id)).where(Subscription.status == "active")
        )
        active_subscribers = active_result.scalar() or 0

        # Calculate MRR
        mrr_result = await db.execute(
            select(func.sum(Subscription.monthly_price)).where(Subscription.status == "active")
        )
        mrr = float(mrr_result.scalar() or 0)

        # Get this month and last month analytics
        this_month = datetime.utcnow().strftime("%Y-%m")
        last_month = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m")

        this_month_result = await db.execute(
            select(RevenueAnalytics).where(RevenueAnalytics.period_key == this_month)
        )
        this_month_data = this_month_result.scalar_one_or_none()

        last_month_result = await db.execute(
            select(RevenueAnalytics).where(RevenueAnalytics.period_key == last_month)
        )
        last_month_data = last_month_result.scalar_one_or_none()

        growth_rate = 0.0
        if last_month_data and last_month_data.total_revenue > 0 and this_month_data:
            growth_rate = (this_month_data.total_revenue - last_month_data.total_revenue) / last_month_data.total_revenue

        churn_rate = 0.0
        if this_month_data and this_month_data.active_subscribers > 0:
            churn_rate = this_month_data.churned_subscribers / this_month_data.active_subscribers

        return {
            "mrr": round(mrr, 2),
            "arr": round(mrr * 12, 2),
            "growth_rate": round(growth_rate, 4),
            "churn_rate": round(churn_rate, 4),
            "active_subscribers": active_subscribers,
            "new_subscribers": this_month_data.new_subscribers if this_month_data else 0,
            "churned_subscribers": this_month_data.churned_subscribers if this_month_data else 0,
        }

    @staticmethod
    async def get_arpu(db: AsyncSession) -> Dict[str, Any]:
        """Get average revenue per user."""
        # Total paying users
        paying_result = await db.execute(
            select(func.count(Subscription.id)).where(Subscription.status == "active")
        )
        paying_users = paying_result.scalar() or 0

        # Total revenue
        revenue_result = await db.execute(
            select(func.sum(Subscription.monthly_price)).where(Subscription.status == "active")
        )
        total_revenue = float(revenue_result.scalar() or 0)

        # Total users
        users_result = await db.execute(select(func.count(User.id)))
        total_users = users_result.scalar() or 0

        overall_arpu = total_revenue / paying_users if paying_users > 0 else 0

        # ARPU by plan
        plan_result = await db.execute(
            select(Subscription.plan, func.sum(Subscription.monthly_price), func.count(Subscription.id))
            .where(Subscription.status == "active")
            .group_by(Subscription.plan)
        )
        plan_rows = plan_result.all()
        arpu_by_plan = {}
        for row in plan_rows:
            plan, revenue, count = row
            arpu_by_plan[plan] = round(revenue / count, 2) if count > 0 else 0

        return {
            "overall_arpu": round(overall_arpu, 2),
            "arpu_by_plan": arpu_by_plan,
            "total_users": total_users,
            "paying_users": paying_users,
        }

    @staticmethod
    async def get_ltv(db: AsyncSession) -> Dict[str, Any]:
        """Get lifetime value analysis."""
        result = await db.execute(select(RevenuePerUser))
        user_revenues = result.scalars().all()

        if not user_revenues:
            return {
                "overall_ltv": 0,
                "ltv_by_plan": {},
                "avg_subscription_months": 0,
                "total_lifetime_revenue": 0,
            }

        total_ltv = sum(u.ltv for u in user_revenues)
        total_months = sum(u.subscription_months for u in user_revenues)
        total_revenue = sum(u.total_revenue for u in user_revenues)

        return {
            "overall_ltv": round(total_ltv / len(user_revenues), 2),
            "ltv_by_plan": {},  # Would need plan data
            "avg_subscription_months": round(total_months / len(user_revenues), 1),
            "total_lifetime_revenue": round(total_revenue, 2),
        }

    @staticmethod
    async def get_payment_failures(db: AsyncSession, limit: int = 50) -> Dict[str, Any]:
        """Get payment failure analysis."""
        # Count failures
        fail_result = await db.execute(
            select(func.count(PaymentTransaction.id)).where(PaymentTransaction.status == "failed")
        )
        total_failures = fail_result.scalar() or 0

        # Total failed amount
        amount_result = await db.execute(
            select(func.sum(PaymentTransaction.amount)).where(PaymentTransaction.status == "failed")
        )
        total_failed_amount = float(amount_result.scalar() or 0)

        # Success count for recovery rate
        success_result = await db.execute(
            select(func.count(PaymentTransaction.id)).where(PaymentTransaction.status == "success")
        )
        total_success = success_result.scalar() or 0

        recovery_rate = total_success / (total_success + total_failures) if (total_success + total_failures) > 0 else 0

        # Recent failures
        recent_result = await db.execute(
            select(PaymentTransaction)
            .where(PaymentTransaction.status == "failed")
            .order_by(PaymentTransaction.processed_at.desc())
            .limit(limit)
        )
        recent_failures = recent_result.scalars().all()

        return {
            "total_failures": total_failures,
            "total_failed_amount": round(total_failed_amount, 2),
            "recovery_rate": round(recovery_rate, 4),
            "recent_failures": [
                {
                    "transaction_id": f.id,
                    "user_id": f.user_id,
                    "amount": f.amount,
                    "failure_reason": f.failure_reason or "Unknown",
                    "processed_at": f.processed_at.isoformat(),
                }
                for f in recent_failures
            ],
        }

    @staticmethod
    async def get_revenue_forecast(db: AsyncSession, months: int = 12) -> Dict[str, Any]:
        """Get revenue forecast (simple linear projection)."""
        metrics = await RevenueService.get_subscription_metrics(db)
        current_mrr = metrics["mrr"]
        growth_rate = metrics["growth_rate"] if metrics["growth_rate"] > 0 else 0.05  # Default 5%

        forecast = []
        projected_mrr = current_mrr
        for i in range(1, months + 1):
            projected_mrr = projected_mrr * (1 + growth_rate)
            confidence_lower = projected_mrr * 0.8
            confidence_upper = projected_mrr * 1.2
            month_date = (datetime.utcnow() + timedelta(days=30 * i)).strftime("%Y-%m")
            forecast.append({
                "period": month_date,
                "projected_revenue": round(projected_mrr, 2),
                "confidence_lower": round(confidence_lower, 2),
                "confidence_upper": round(confidence_upper, 2),
            })

        return {
            "current_mrr": round(current_mrr, 2),
            "projected_mrr_3m": round(forecast[2]["projected_revenue"], 2) if len(forecast) > 2 else 0,
            "projected_mrr_6m": round(forecast[5]["projected_revenue"], 2) if len(forecast) > 5 else 0,
            "projected_mrr_12m": round(forecast[11]["projected_revenue"], 2) if len(forecast) > 11 else 0,
            "growth_assumption": round(growth_rate, 4),
            "forecast": forecast,
        }


revenue_service = RevenueService()
