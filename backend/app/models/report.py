from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime


class ReportDefinition(Base):
    """Custom report definitions."""
    __tablename__ = "report_definitions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)
    data_source: Mapped[str] = mapped_column(String(100), nullable=False)
    filters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    columns: Mapped[list | None] = mapped_column(JSON, nullable=True)
    aggregations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    group_by: Mapped[list | None] = mapped_column(JSON, nullable=True)
    sort_by: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_public: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", backref="reports")


class ReportSchedule(Base):
    """Scheduled report generation."""
    __tablename__ = "report_schedules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("report_definitions.id"), nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    next_run: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_run: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    recipients: Mapped[list | None] = mapped_column(JSON, nullable=True)
    format: Mapped[str] = mapped_column(String(20), default="pdf")
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    report = relationship("ReportDefinition", backref="schedules")


class ReportExecution(Base):
    """Report execution history."""
    __tablename__ = "report_executions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("report_definitions.id"), nullable=False)
    executed_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    report = relationship("ReportDefinition", backref="executions")
    executor = relationship("User", backref="report_executions")


class ReportShare(Base):
    """Report sharing permissions."""
    __tablename__ = "report_shares"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("report_definitions.id"), nullable=False)
    shared_with_user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    shared_with_role: Mapped[str | None] = mapped_column(String(50), nullable=True)
    permission: Mapped[str] = mapped_column(String(20), default="view")
    shared_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    report = relationship("ReportDefinition", backref="shares")
    shared_with_user = relationship("User", foreign_keys=[shared_with_user_id])
    shared_by_user = relationship("User", foreign_keys=[shared_by])


class DashboardConfig(Base):
    """Dashboard customization settings."""
    __tablename__ = "dashboard_configs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    layout: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    widgets: Mapped[list | None] = mapped_column(JSON, nullable=True)
    filters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    refresh_interval: Mapped[int] = mapped_column(Integer, default=300)
    theme: Mapped[str] = mapped_column(String(20), default="dark")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="dashboard_config")
