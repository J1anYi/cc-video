from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, require_admin
from app.schemas.predictions import (
    ContentSuccessPrediction,
    DemandForecastResponse,
    LtvPrediction,
    PricingSuggestionResponse,
    ContentGapResponse,
)
from app.services.prediction_service import prediction_service

router = APIRouter(prefix="/admin/predictions", tags=["predictions"])


@router.get("/content/{content_id}/success", response_model=ContentSuccessPrediction)
async def predict_content_success(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return ContentSuccessPrediction(**await prediction_service.predict_content_success(db, content_id))


@router.get("/demand", response_model=DemandForecastResponse)
async def forecast_demand(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return DemandForecastResponse(**await prediction_service.forecast_demand(db, days))


@router.get("/ltv/{user_id}", response_model=LtvPrediction)
async def predict_ltv(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return LtvPrediction(**await prediction_service.predict_ltv(db, user_id))


@router.get("/pricing", response_model=PricingSuggestionResponse)
async def suggest_pricing(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return PricingSuggestionResponse(**await prediction_service.suggest_pricing(db))


@router.get("/content-gaps", response_model=ContentGapResponse)
async def analyze_content_gaps(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    return ContentGapResponse(**await prediction_service.analyze_content_gaps(db))
