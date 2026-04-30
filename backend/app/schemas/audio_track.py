from pydantic import BaseModel
from typing import List, Optional

class AudioTrackBase(BaseModel):
    language: str
    title: Optional[str] = None
    is_default: bool = False
    is_original: bool = False

class AudioTrackCreate(AudioTrackBase):
    pass

class AudioTrackResponse(AudioTrackBase):
    id: int
    video_file_id: int
    channel_layout: str
    codec: str
    bitrate: int
    sample_rate: int
    class Config:
        from_attributes = True

class AudioTracksListResponse(BaseModel):
    video_file_id: int
    tracks: List[AudioTrackResponse]
