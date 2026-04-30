from .manager import manager
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NotificationHandler:
    async def push_notification(self, user_id: int, notification: Dict[str, Any]):
        message = {
            "type": "notification",
            "data": notification,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await manager.send_to_user(user_id, message)
        logger.info(f"Pushed notification to user {user_id}")

    async def push_notification_batch(self, user_ids: list[int], notification: Dict[str, Any]):
        message = {
            "type": "notification",
            "data": notification,
            "timestamp": datetime.utcnow().isoformat(),
        }
        for user_id in user_ids:
            await manager.send_to_user(user_id, message)

    async def update_unread_count(self, user_id: int, count: int):
        message = {
            "type": "unread_count",
            "count": count,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await manager.send_to_user(user_id, message)

    async def notification_acknowledged(self, user_id: int, notification_id: int):
        message = {
            "type": "notification_ack",
            "notification_id": notification_id,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await manager.send_to_user(user_id, message)


notification_handler = NotificationHandler()
