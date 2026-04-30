from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ContentSuccessPrediction(BaseModel):
    content_id: int
    title: str
    success_score: float
    predicted_views: int
    confidence: float
    factors: Optional[Dict[str, Any]] = None


class DemandForecastPoint(BaseModel):
    date: str
    predicted_views: int
    predicted_hours: int
    confidence: float


class DemandForecastResponse(BaseModel):
    forecasts: List[DemandForecastPoint]
    total_predicted_views: int


class LtvPrediction(BaseModel):
    user_id: int
    predicted_ltv: float
    confidence: float
    factors: Optional[Dict[str, Any]] = None


class PricingSuggestionItem(BaseModel):
    plan: str
    current_price: float
    suggested_price: float
    expected_revenue_change: float
    reasoning: Optional[str] = None


class PricingSuggestionResponse(BaseModel):
    suggestions: List[PricingSuggestionItem]


class ContentGapItem(BaseModel):
    genre: str
    demand_score: float
    supply_score: float
    gap_score: float
    recommendation: Optional[str] = None


class ContentGapResponse(BaseModel):
    gaps: List[ContentGapItem]
