from datetime import datetime
from pydantic import BaseModel


class VideoFileResponse(BaseModel):
    """Schema for video file responses.

    Note: file_path is intentionally excluded as it's an internal storage detail.
    """

    id: int
    movie_id: int
    filename: str  # Original uploaded filename
    file_size: int  # Size in bytes
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True
