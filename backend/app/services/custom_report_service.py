from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta
from typing import Any

from app.models.report import ReportDefinition, ReportSchedule, ReportExecution, ReportShare, DashboardConfig


class CustomReportService:
    """Service for custom report builder operations."""

    async def create_report(self, db: AsyncSession, name: str, report_type: str,
                           data_source: str, created_by: int, description: str | None = None,
                           filters: dict | None = None, columns: list | None = None,
                           aggregations: dict | None = None, group_by: list | None = None,
                           sort_by: dict | None = None, is_public: bool = False) -> ReportDefinition:
        report = ReportDefinition(name=name, description=description, report_type=report_type,
                                 data_source=data_source, filters=filters, columns=columns,
                                 aggregations=aggregations, group_by=group_by, sort_by=sort_by,
                                 is_public=is_public, created_by=created_by)
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    async def get_reports(self, db: AsyncSession, user_id: int, include_public: bool = True) -> list[ReportDefinition]:
        query = select(ReportDefinition)
        if include_public:
            query = query.where(or_(ReportDefinition.created_by == user_id, ReportDefinition.is_public == True))
        else:
            query = query.where(ReportDefinition.created_by == user_id)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_report(self, db: AsyncSession, report_id: int) -> ReportDefinition | None:
        result = await db.execute(select(ReportDefinition).where(ReportDefinition.id == report_id))
        return result.scalar_one_or_none()

    async def execute_report(self, db: AsyncSession, report_id: int, executed_by: int | None = None,
                            parameters: dict | None = None) -> dict:
        report = await self.get_report(db, report_id)
        if not report:
            return {"error": "Report not found"}
        execution = ReportExecution(report_id=report_id, executed_by=executed_by, status="running", parameters=parameters)
        db.add(execution)
        await db.commit()
        try:
            data = await self._generate_report_data(db, report, parameters)
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
            execution.row_count = len(data.get("rows", []))
            await db.commit()
            return {"execution_id": execution.id, "status": "completed", "row_count": execution.row_count, "data": data}
        except Exception as e:
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await db.commit()
            return {"error": str(e), "execution_id": execution.id}

    async def _generate_report_data(self, db: AsyncSession, report: ReportDefinition, parameters: dict | None = None) -> dict:
        if report.report_type == "content":
            return {"columns": ["Title", "Views", "Completion Rate", "Revenue"],
                    "rows": [["Movie A", 15000, 0.85, 1200.00], ["Movie B", 12000, 0.78, 980.00], ["Movie C", 8000, 0.92, 750.00]],
                    "total_rows": 3}
        elif report.report_type == "user":
            return {"columns": ["User", "Watch Hours", "Sessions", "LTV"],
                    "rows": [["user1@example.com", 45.5, 32, 89.00], ["user2@example.com", 32.1, 28, 65.00], ["user3@example.com", 78.2, 45, 120.00]],
                    "total_rows": 3}
        elif report.report_type == "revenue":
            return {"columns": ["Month", "Revenue", "Subscriptions", "Churn"],
                    "rows": [["Jan 2026", 45000, 1200, 0.05], ["Feb 2026", 48500, 1280, 0.04], ["Mar 2026", 52000, 1350, 0.03]],
                    "total_rows": 3}
        return {"columns": [], "rows": [], "total_rows": 0}

    async def schedule_report(self, db: AsyncSession, report_id: int, frequency: str, recipients: list[str], format: str = "pdf") -> ReportSchedule:
        next_run = self._calculate_next_run(frequency)
        schedule = ReportSchedule(report_id=report_id, frequency=frequency, next_run=next_run, recipients=recipients, format=format)
        db.add(schedule)
        await db.commit()
        await db.refresh(schedule)
        return schedule

    def _calculate_next_run(self, frequency: str) -> datetime:
        now = datetime.utcnow()
        if frequency == "daily": return now + timedelta(days=1)
        elif frequency == "weekly": return now + timedelta(weeks=1)
        elif frequency == "monthly": return now + timedelta(days=30)
        return now

    async def get_schedules(self, db: AsyncSession, report_id: int) -> list[ReportSchedule]:
        result = await db.execute(select(ReportSchedule).where(ReportSchedule.report_id == report_id))
        return list(result.scalars().all())

    async def share_report(self, db: AsyncSession, report_id: int, shared_by: int, shared_with_user_id: int | None = None,
                          shared_with_role: str | None = None, permission: str = "view") -> ReportShare:
        share = ReportShare(report_id=report_id, shared_with_user_id=shared_with_user_id,
                           shared_with_role=shared_with_role, permission=permission, shared_by=shared_by)
        db.add(share)
        await db.commit()
        await db.refresh(share)
        return share

    async def get_shares(self, db: AsyncSession, report_id: int) -> list[ReportShare]:
        result = await db.execute(select(ReportShare).where(ReportShare.report_id == report_id))
        return list(result.scalars().all())

    async def get_dashboard_config(self, db: AsyncSession, user_id: int) -> DashboardConfig | None:
        result = await db.execute(select(DashboardConfig).where(DashboardConfig.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_dashboard_config(self, db: AsyncSession, user_id: int, layout: dict | None = None,
                                     widgets: list | None = None, filters: dict | None = None,
                                     refresh_interval: int | None = None, theme: str | None = None) -> DashboardConfig:
        config = await self.get_dashboard_config(db, user_id)
        if not config:
            config = DashboardConfig(user_id=user_id)
            db.add(config)
        if layout is not None: config.layout = layout
        if widgets is not None: config.widgets = widgets
        if filters is not None: config.filters = filters
        if refresh_interval is not None: config.refresh_interval = refresh_interval
        if theme is not None: config.theme = theme
        await db.commit()
        await db.refresh(config)
        return config

    async def export_report(self, db: AsyncSession, report_id: int, format: str) -> dict:
        result = await self.execute_report(db, report_id)
        if "error" in result: return result
        data = result.get("data", {})
        if format == "csv":
            return {"format": "csv", "content": self._to_csv(data)}
        elif format == "xlsx":
            return {"format": "xlsx", "content": "Excel export placeholder"}
        return {"format": "pdf", "content": "PDF export placeholder"}

    def _to_csv(self, data: dict) -> str:
        columns = data.get("columns", [])
        rows = data.get("rows", [])
        lines = [",".join(columns)]
        for row in rows: lines.append(",".join(str(v) for v in row))
        return "\n".join(lines)


custom_report_service = CustomReportService()
