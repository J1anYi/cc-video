from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import math

from app.dependencies import get_db, get_current_user
from app.middleware.rbac import require_roles
from app.models.user import User
from app.schemas.report import (
    ReportCreate, ReportResponse, ReportListResponse,
    ReportActionRequest, ReportStatsResponse
)
from app.services.report import report_service


router = APIRouter(prefix="/reports", tags=["reports"])
admin_required = Depends(require_roles(["admin"]))


@router.post("", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Report inappropriate content."""
    report = await report_service.create_report(
        db,
        current_user.id,
        report_data.content_type,
        report_data.content_id,
        report_data.reason,
    )
    return ReportResponse.model_validate(report)


@router.get("/admin", response_model=ReportListResponse, dependencies=[admin_required])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """List pending reports. Admin only."""
    reports, total = await report_service.get_pending_reports(db, page, limit)
    return ReportListResponse(
        reports=[ReportResponse.model_validate(r) for r in reports],
        total=total,
        page=page,
        limit=limit,
    )


@router.get("/admin/stats", response_model=ReportStatsResponse, dependencies=[admin_required])
async def get_report_stats(db: AsyncSession = Depends(get_db)):
    """Get report statistics. Admin only."""
    stats = await report_service.get_report_stats(db)
    return ReportStatsResponse(**stats)


@router.patch("/admin/{report_id}/dismiss", response_model=ReportResponse, dependencies=[admin_required])
async def dismiss_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Dismiss a report. Admin only."""
    report = await report_service.dismiss_report(db, report_id, current_user.id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse.model_validate(report)


@router.patch("/admin/{report_id}/action", response_model=ReportResponse, dependencies=[admin_required])
async def action_report(
    report_id: int,
    action_data: ReportActionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Take action on a report. Admin only."""
    report = await report_service.action_report(
        db, report_id, current_user.id,
        action_data.remove_content, action_data.warn_user
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportResponse.model_validate(report)
