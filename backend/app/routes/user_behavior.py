from fastapi import APIRouter, Depends, Query, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.dependencies import get_db, require_admin
from app.schemas.user_behavior import (
    UserJourneyResponse,
    SessionMetricsResponse,
    SegmentResponse,
    CreateSegmentRequest,
    CohortResponse,
    ChurnRiskUserResponse,
)
from app.services.user_behavior_service import user_behavior_service

router = APIRouter(prefix="/admin/analytics", tags=["user-behavior"])


@router.post("/journey/track")
async def track_journey_event(
    user_id: int = Body(...),
    session_id: str = Body(...),
    event_type: str = Body(...),
    event_data: Optional[dict] = Body(None),
    page_url: str = Body(""),
    referrer_url: Optional[str] = Body(None),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Track a user journey event."""
    event = await user_behavior_service.track_event(
        db, user_id, session_id, event_type, event_data, page_url, referrer_url
    )
    return {"success": True, "event_id": event.id}


@router.get("/journeys/{user_id}", response_model=UserJourneyResponse)
async def get_user_journey(
    user_id: int,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get user's journey events."""
    journey = await user_behavior_service.get_user_journey(db, user_id, limit)
    return UserJourneyResponse(**journey)


@router.get("/sessions", response_model=SessionMetricsResponse)
async def get_session_metrics(
    user_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get session analytics metrics."""
    metrics = await user_behavior_service.get_session_metrics(db, user_id)
    return SessionMetricsResponse(**metrics)


@router.get("/segments", response_model=List[SegmentResponse])
async def get_segments(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """List all user segments."""
    segments = await user_behavior_service.get_segments(db)
    return [SegmentResponse(**s) for s in segments]


@router.post("/segments", response_model=SegmentResponse)
async def create_segment(
    request: CreateSegmentRequest,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Create a new user segment."""
    rules = [r.model_dump() for r in request.rules]
    segment = await user_behavior_service.create_segment(
        db, request.name, request.description, rules
    )
    return SegmentResponse(
        id=segment.id,
        name=segment.name,
        description=segment.description,
        rules=segment.rules.get("rules", []) if segment.rules else [],
        member_count=segment.member_count,
        created_at=segment.created_at.isoformat(),
    )


@router.get("/cohorts", response_model=List[CohortResponse])
async def get_cohort_analytics(
    weeks: int = Query(12, ge=1, le=52),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get cohort retention analytics."""
    cohorts = await user_behavior_service.get_cohort_analytics(db, weeks)
    return [CohortResponse(**c) for c in cohorts]


@router.get("/churn", response_model=List[ChurnRiskUserResponse])
async def get_churn_risk_users(
    threshold: float = Query(50.0, ge=0, le=100),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
):
    """Get users at risk of churn."""
    users = await user_behavior_service.get_at_risk_users(db, threshold, limit)
    return [ChurnRiskUserResponse(**u) for u in users]
