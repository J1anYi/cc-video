from pydantic import BaseModel
from typing import List, Optional


class RevenueTrendPoint(BaseModel):
    period: str
    total_revenue: float
    new_revenue: float
    churned_revenue: float
    net_revenue: float


class RevenueTrendsResponse(BaseModel):
    period_type: str
    data: List[RevenueTrendPoint]


class SubscriptionMetricsResponse(BaseModel):
    mrr: float
    arr: float
    growth_rate: float
    churn_rate: float
    active_subscribers: int
    new_subscribers: int
    churned_subscribers: int


class ArpuResponse(BaseModel):
    overall_arpu: float
    arpu_by_plan: dict
    total_users: int
    paying_users: int


class LtvResponse(BaseModel):
    overall_ltv: float
    ltv_by_plan: dict
    avg_subscription_months: float
    total_lifetime_revenue: float


class PaymentFailureItem(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    failure_reason: str
    processed_at: str


class PaymentFailuresResponse(BaseModel):
    total_failures: int
    total_failed_amount: float
    recovery_rate: float
    recent_failures: List[PaymentFailureItem]


class ForecastPoint(BaseModel):
    period: str
    projected_revenue: float
    confidence_lower: float
    confidence_upper: float


class RevenueForecastResponse(BaseModel):
    current_mrr: float
    projected_mrr_3m: float
    projected_mrr_6m: float
    projected_mrr_12m: float
    growth_assumption: float
    forecast: List[ForecastPoint]
