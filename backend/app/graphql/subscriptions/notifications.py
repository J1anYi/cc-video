import strawberry
from typing import AsyncGenerator
from datetime import datetime
from strawberry.types import Info


@strawberry.type
class NotificationType:
    id: int
    message: str
    created_at: datetime


@strawberry.type
class NotificationSubscription:
    @strawberry.subscription
    async def notifications(self, info: Info) -> AsyncGenerator[NotificationType, None]:
        user = info.context.get("user")
        if not user:
            return
        
        # Placeholder - in production, connect to notification service
        yield NotificationType(
            id=1,
            message="Welcome to notifications",
            created_at=datetime.utcnow(),
        )
