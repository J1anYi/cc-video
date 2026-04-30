from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, require_admin
from app.schemas.revenue import (
    RevenueTrendsResponse,
    SubscriptionMetricsResponse,
    ArpuResponse,
    LtvResponse,
    PaymentFailuresResponse,
    RevenueForecastResponse,
)
from app.services.revenue_service import revenue_service

router = APIRouter(prefix="/admin/analytics/revenue", tags=["revenue"])


@router.get("/trends", response_model=RevenueTrendsResponse)
async def get_revenue_trends(
    period_type: str = Query("monthly"),
    periods: int = Query(12),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return RevenueTrendsResponse(**await revenue_service.get_revenue_trends(db, period_type, periods))


@router.get("/metrics", response_model=SubscriptionMetricsResponse)
async def get_subscription_metrics(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return SubscriptionMetricsResponse(**await revenue_service.get_subscription_metrics(db))


@router.get("/arpu", response_model=ArpuResponse)
async def get_arpu(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return ArpuResponse(**await revenue_service.get_arpu(db))


@router.get("/ltv", response_model=LtvResponse)
async def get_ltv(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return LtvResponse(**await revenue_service.get_ltv(db))


@router.get("/failures", response_model=PaymentFailuresResponse)
async def get_payment_failures(
    limit: int = Query(50),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return PaymentFailuresResponse(**await revenue_service.get_payment_failures(db, limit))


@router.get("/forecast", response_model=RevenueForecastResponse)
async def get_revenue_forecast(
    months: int = Query(12),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return RevenueForecastResponse(**await revenue_service.get_revenue_forecast(db, months))
