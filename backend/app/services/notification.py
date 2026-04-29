from datetime import datetime
from typing import List
from sqlalchemy import select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.notification import Notification, NotificationType
from app.models.user import User


class NotificationService:
    async def create_notification(
        self,
        db: AsyncSession,
        user_id: int,
        notification_type: str,
        title: str,
        content: str | None = None,
        actor_id: int | None = None,
        target_type: str | None = None,
        target_id: int | None = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            actor_id=actor_id,
            notification_type=notification_type,
            title=title,
            content=content,
            target_type=target_type,
            target_id=target_id,
            created_at=datetime.utcnow(),
        )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    async def get_notifications(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ) -> tuple[List[Notification], int, int]:
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read == False)
        query = query.order_by(Notification.created_at.desc())

        result = await db.execute(query.offset(skip).limit(limit))
        notifications = list(result.scalars().all())

        count_query = select(func.count(Notification.id)).where(Notification.user_id == user_id)
        if unread_only:
            count_query = count_query.where(Notification.is_read == False)
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        unread_result = await db.execute(
            select(func.count(Notification.id)).where(
                and_(Notification.user_id == user_id, Notification.is_read == False)
            )
        )
        unread_count = unread_result.scalar() or 0

        return notifications, total, unread_count

    async def mark_as_read(self, db: AsyncSession, user_id: int, notification_id: int) -> bool:
        result = await db.execute(
            update(Notification)
            .where(and_(Notification.id == notification_id, Notification.user_id == user_id))
            .values(is_read=True)
        )
        await db.commit()
        return result.rowcount > 0

    async def mark_all_as_read(self, db: AsyncSession, user_id: int) -> int:
        result = await db.execute(
            update(Notification)
            .where(and_(Notification.user_id == user_id, Notification.is_read == False))
            .values(is_read=True)
        )
        await db.commit()
        return result.rowcount

    async def get_unread_count(self, db: AsyncSession, user_id: int) -> int:
        result = await db.execute(
            select(func.count(Notification.id)).where(
                and_(Notification.user_id == user_id, Notification.is_read == False)
            )
        )
        return result.scalar() or 0


notification_service = NotificationService()
