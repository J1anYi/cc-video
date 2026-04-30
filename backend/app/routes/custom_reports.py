from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_db
from app.dependencies import require_admin
from app.services.custom_report_service import custom_report_service

router = APIRouter(prefix="/admin/reports", tags=["Custom Reports"])


class ReportCreate(BaseModel):
    name: str
    report_type: str
    data_source: str
    description: Optional[str] = None
    filters: Optional[dict] = None
    columns: Optional[list] = None
    aggregations: Optional[dict] = None
    group_by: Optional[list] = None
    sort_by: Optional[dict] = None
    is_public: bool = False


class ScheduleCreate(BaseModel):
    frequency: str
    recipients: list[str]
    format: str = "pdf"


class ShareCreate(BaseModel):
    shared_with_user_id: Optional[int] = None
    shared_with_role: Optional[str] = None
    permission: str = "view"


class DashboardConfigUpdate(BaseModel):
    layout: Optional[dict] = None
    widgets: Optional[list] = None
    filters: Optional[dict] = None
    refresh_interval: Optional[int] = None
    theme: Optional[str] = None


@router.post("")
async def create_report(data: ReportCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    report = await custom_report_service.create_report(
        db, name=data.name, report_type=data.report_type, data_source=data.data_source,
        description=data.description, filters=data.filters, columns=data.columns,
        aggregations=data.aggregations, group_by=data.group_by, sort_by=data.sort_by,
        is_public=data.is_public, created_by=admin.id
    )
    return {"id": report.id, "name": report.name, "report_type": report.report_type}


@router.get("")
async def list_reports(db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    reports = await custom_report_service.get_reports(db, admin.id)
    return [{"id": r.id, "name": r.name, "report_type": r.report_type, "is_public": r.is_public,
             "created_at": r.created_at.isoformat()} for r in reports]


@router.get("/{report_id}")
async def get_report(report_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    report = await custom_report_service.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"id": report.id, "name": report.name, "report_type": report.report_type,
            "description": report.description, "data_source": report.data_source,
            "filters": report.filters, "columns": report.columns, "is_public": report.is_public}


@router.post("/{report_id}/execute")
async def execute_report(report_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    result = await custom_report_service.execute_report(db, report_id, executed_by=admin.id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{report_id}/export")
async def export_report(report_id: int, format: str = "pdf", db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    result = await custom_report_service.export_report(db, report_id, format)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{report_id}/schedule")
async def schedule_report(report_id: int, data: ScheduleCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    schedule = await custom_report_service.schedule_report(db, report_id, data.frequency, data.recipients, data.format)
    return {"id": schedule.id, "frequency": schedule.frequency, "next_run": schedule.next_run.isoformat()}


@router.get("/{report_id}/schedules")
async def get_schedules(report_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    schedules = await custom_report_service.get_schedules(db, report_id)
    return [{"id": s.id, "frequency": s.frequency, "next_run": s.next_run.isoformat(),
             "is_active": s.is_active} for s in schedules]


@router.post("/{report_id}/share")
async def share_report(report_id: int, data: ShareCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    share = await custom_report_service.share_report(db, report_id, admin.id, data.shared_with_user_id,
                                                     data.shared_with_role, data.permission)
    return {"id": share.id, "permission": share.permission}


@router.get("/{report_id}/shares")
async def get_shares(report_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    shares = await custom_report_service.get_shares(db, report_id)
    return [{"id": s.id, "shared_with_user_id": s.shared_with_user_id, "shared_with_role": s.shared_with_role,
             "permission": s.permission} for s in shares]


@router.get("/dashboard/config")
async def get_dashboard_config(db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    config = await custom_report_service.get_dashboard_config(db, admin.id)
    if not config:
        return {"layout": {}, "widgets": [], "filters": {}, "refresh_interval": 300, "theme": "dark"}
    return {"layout": config.layout, "widgets": config.widgets, "filters": config.filters,
            "refresh_interval": config.refresh_interval, "theme": config.theme}


@router.put("/dashboard/config")
async def update_dashboard_config(data: DashboardConfigUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    config = await custom_report_service.update_dashboard_config(
        db, admin.id, layout=data.layout, widgets=data.widgets, filters=data.filters,
        refresh_interval=data.refresh_interval, theme=data.theme
    )
    return {"layout": config.layout, "widgets": config.widgets, "filters": config.filters,
            "refresh_interval": config.refresh_interval, "theme": config.theme}
