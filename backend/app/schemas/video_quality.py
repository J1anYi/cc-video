"""Schemas for video quality endpoints."""

from pydantic import BaseModel
from typing import List


class VideoQualityResponse(BaseModel):
    quality: str
    width: int
    height: int
    bitrate: int
    resolution: str


class VideoQualitiesListResponse(BaseModel):
    video_file_id: int
    qualities: List[VideoQualityResponse]


class TranscodingStatusResponse(BaseModel):
    video_file_id: int
    status: str
    qualities_completed: List[str]
    qualities_pending: List[str]
    progress_percent: int
