from datetime import datetime
from pydantic import BaseModel


class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBriefResponse(BaseModel):
    id: int
    email: str
    display_name: str | None

    class Config:
        from_attributes = True


class FollowerResponse(BaseModel):
    id: int
    follower: UserBriefResponse
    created_at: datetime

    class Config:
        from_attributes = True


class FollowingResponse(BaseModel):
    id: int
    following: UserBriefResponse
    created_at: datetime

    class Config:
        from_attributes = True


class FollowStatusResponse(BaseModel):
    is_following: bool


class FollowCountsResponse(BaseModel):
    followers_count: int
    following_count: int
