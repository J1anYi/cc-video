from datetime import datetime
from pydantic import BaseModel
from app.models.report import ContentType, ReportStatus


class ReportCreate(BaseModel):
    content_type: ContentType
    content_id: int
    reason: str


class ReportResponse(BaseModel):
    id: int
    reporter_id: int
    content_type: ContentType
    content_id: int
    reason: str
    status: ReportStatus
    created_at: datetime
    reviewed_at: datetime | None = None

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    reports: list[ReportResponse]
    total: int
    page: int
    limit: int


class ReportActionRequest(BaseModel):
    remove_content: bool = True
    warn_user: bool = False


class ReportStatsResponse(BaseModel):
    pending: int
    dismissed: int
    actioned: int
    total: int
