from datetime import datetime
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Comment content")


class CommentResponse(BaseModel):
    id: int
    user_id: int
    review_id: int
    username: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]
    total: int
