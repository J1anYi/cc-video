from datetime import datetime
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.report import Report, ContentType, ReportStatus
from app.models.review import Review
from app.models.comment import Comment
from app.models.user import User


class ReportService:
    async def create_report(
        self,
        db: AsyncSession,
        reporter_id: int,
        content_type: ContentType,
        content_id: int,
        reason: str,
    ) -> Report:
        """Create a new report."""
        report = Report(
            reporter_id=reporter_id,
            content_type=content_type,
            content_id=content_id,
            reason=reason,
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    async def get_pending_reports(
        self,
        db: AsyncSession,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Report], int]:
        """Get pending reports with pagination."""
        query = (
            select(Report)
            .where(Report.status == ReportStatus.PENDING)
            .options(selectinload(Report.reporter))
            .order_by(Report.created_at.desc())
        )

        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar()

        query = query.offset((page - 1) * limit).limit(limit)
        result = await db.execute(query)
        reports = list(result.scalars().all())

        return reports, total

    async def get_report(self, db: AsyncSession, report_id: int) -> Optional[Report]:
        """Get a report by ID."""
        result = await db.execute(
            select(Report)
            .where(Report.id == report_id)
            .options(selectinload(Report.reporter))
        )
        return result.scalar_one_or_none()

    async def dismiss_report(
        self,
        db: AsyncSession,
        report_id: int,
        reviewer_id: int,
    ) -> Optional[Report]:
        """Dismiss a report (content is acceptable)."""
        report = await self.get_report(db, report_id)
        if not report:
            return None

        report.status = ReportStatus.DISMISSED
        report.reviewed_at = datetime.utcnow()
        report.reviewed_by = reviewer_id
        await db.commit()
        await db.refresh(report)
        return report

    async def action_report(
        self,
        db: AsyncSession,
        report_id: int,
        reviewer_id: int,
        remove_content: bool = True,
        warn_user: bool = False,
    ) -> Optional[Report]:
        """Take action on a report."""
        report = await self.get_report(db, report_id)
        if not report:
            return None

        if remove_content:
            if report.content_type == ContentType.REVIEW:
                review = (await db.execute(select(Review).where(Review.id == report.content_id))).scalar_one_or_none()
                if review:
                    author_id = review.user_id
                    await db.delete(review)
                    if warn_user:
                        await self._increment_warnings(db, author_id)
            elif report.content_type == ContentType.COMMENT:
                comment = (await db.execute(select(Comment).where(Comment.id == report.content_id))).scalar_one_or_none()
                if comment:
                    author_id = comment.user_id
                    await db.delete(comment)
                    if warn_user:
                        await self._increment_warnings(db, author_id)
        elif warn_user:
            if report.content_type == ContentType.REVIEW:
                review = (await db.execute(select(Review).where(Review.id == report.content_id))).scalar_one_or_none()
                if review:
                    await self._increment_warnings(db, review.user_id)
            elif report.content_type == ContentType.COMMENT:
                comment = (await db.execute(select(Comment).where(Comment.id == report.content_id))).scalar_one_or_none()
                if comment:
                    await self._increment_warnings(db, comment.user_id)

        report.status = ReportStatus.ACTIONED
        report.reviewed_at = datetime.utcnow()
        report.reviewed_by = reviewer_id
        await db.commit()
        await db.refresh(report)
        return report

    async def _increment_warnings(self, db: AsyncSession, user_id: int) -> None:
        """Increment user's warning count."""
        user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
        if user:
            user.warnings_count = (user.warnings_count or 0) + 1
            await db.commit()

    async def get_report_stats(self, db: AsyncSession) -> dict:
        """Get report statistics."""
        pending = (await db.execute(
            select(func.count()).where(Report.status == ReportStatus.PENDING)
        )).scalar()
        dismissed = (await db.execute(
            select(func.count()).where(Report.status == ReportStatus.DISMISSED)
        )).scalar()
        actioned = (await db.execute(
            select(func.count()).where(Report.status == ReportStatus.ACTIONED)
        )).scalar()
        return {
            "pending": pending,
            "dismissed": dismissed,
            "actioned": actioned,
            "total": pending + dismissed + actioned,
        }


report_service = ReportService()
