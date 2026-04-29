from datetime import datetime
from pydantic import BaseModel


class ActivityResponse(BaseModel):
    id: int
    user_id: int
    username: str | None
    activity_type: str
    movie_id: int | None
    movie_title: str | None
    reference_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityListResponse(BaseModel):
    activities: list[ActivityResponse]
    total: int
