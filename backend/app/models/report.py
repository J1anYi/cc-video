from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class ContentType(str, enum.Enum):
    REVIEW = "review"
    COMMENT = "comment"


class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    DISMISSED = "dismissed"
    ACTIONED = "actioned"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    content_type: Mapped[ContentType] = mapped_column(SQLEnum(ContentType), nullable=False)
    content_id: Mapped[int] = mapped_column(nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus), default=ReportStatus.PENDING, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Relationships
    reporter: Mapped["User"] = relationship("User", foreign_keys=[reporter_id])
    reviewer: Mapped["User | None"] = relationship("User", foreign_keys=[reviewed_by])
