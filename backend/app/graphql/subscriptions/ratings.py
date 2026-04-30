import strawberry
from typing import AsyncGenerator
from datetime import datetime
from strawberry.types import Info


@strawberry.type
class RatingUpdateType:
    movie_id: int
    new_rating: float
    updated_at: datetime


@strawberry.type
class RatingSubscription:
    @strawberry.subscription
    async def rating_updates(self, info: Info, movie_id: int) -> AsyncGenerator[RatingUpdateType, None]:
        # Placeholder - in production, connect to rating update events
        yield RatingUpdateType(
            movie_id=movie_id,
            new_rating=4.5,
            updated_at=datetime.utcnow(),
        )
