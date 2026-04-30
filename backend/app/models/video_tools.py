"""Video editing tools models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from app.database import Base


class VideoEditProject(Base):
    """Video editing project."""
    __tablename__ = "video_edit_projects"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=False)
    name = Column(String(200), nullable=False)
    status = Column(String(50), default="draft")  # draft, processing, complete
    timeline = Column(JSON, default=dict)  # tracks, clips, effects
    output_settings = Column(JSON, default=dict)  # resolution, format, codec
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VideoThumbnail(Base):
    """Generated video thumbnail."""
    __tablename__ = "video_thumbnails"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    timestamp = Column(Float, nullable=False)  # seconds
    image_url = Column(String(500), nullable=False)
    is_selected = Column(Boolean, default=False)
    is_auto_generated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoAudioTrack(Base):
    """Multi-language audio track."""
    __tablename__ = "video_audio_tracks"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    language_code = Column(String(10), nullable=False)  # en, zh, es, etc.
    language_name = Column(String(100), nullable=False)  # English, Chinese, Spanish
    audio_url = Column(String(500), nullable=False)
    is_default = Column(Boolean, default=False)
    codec = Column(String(50), default="aac")
    bitrate = Column(Integer, default=128000)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoSubtitle(Base):
    """Video subtitle track."""
    __tablename__ = "video_subtitles"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    language_code = Column(String(10), nullable=False)
    language_name = Column(String(100), nullable=False)
    subtitle_url = Column(String(500), nullable=False)
    format = Column(String(20), default="vtt")  # vtt, srt, ass
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoTemplate(Base):
    """Reusable video editing template."""
    __tablename__ = "video_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default="general")  # intro, outro, transition, effects
    config = Column(JSON, default=dict)  # filters, transitions, overlays
    preview_url = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
