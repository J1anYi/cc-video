"""Music streaming models for Phase 226."""
from datetime import date, datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import String, Text, Integer, Date, DateTime, ForeignKey, Table, Column, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class AlbumType(str, enum.Enum):
    ALBUM = "album"
    SINGLE = "single"
    EP = "ep"


class AudioQuality(str, enum.Enum):
    LOW = "low"       # 64kbps AAC
    MEDIUM = "medium" # 128kbps MP3
    HIGH = "high"     # 256kbps MP3
    LOSSLESS = "lossless"  # FLAC


# Association table for track-genre many-to-many
track_genres = Table(
    "track_genres",
    Base.metadata,
    Column("track_id", ForeignKey("tracks.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


class Artist(Base):
    """Music artist model."""
    __tablename__ = "artists"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    albums: Mapped[List["Album"]] = relationship("Album", back_populates="artist", cascade="all, delete-orphan")


class Album(Base):
    """Music album model."""
    __tablename__ = "albums"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    artist_id: Mapped[str] = mapped_column(String(36), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    release_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cover_art_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    album_type: Mapped[AlbumType] = mapped_column(SQLEnum(AlbumType), default=AlbumType.ALBUM)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    artist: Mapped["Artist"] = relationship("Artist", back_populates="albums")
    tracks: Mapped[List["Track"]] = relationship("Track", back_populates="album", cascade="all, delete-orphan")


class Genre(Base):
    """Music genre model."""
    __tablename__ = "genres"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # Relationships
    tracks: Mapped[List["Track"]] = relationship("Track", secondary=track_genres, back_populates="genres")


class Track(Base):
    """Music track model."""
    __tablename__ = "tracks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    album_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("albums.id", ondelete="SET NULL"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    track_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    disc_number: Mapped[int] = mapped_column(Integer, default=1)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    audio_format: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    bitrate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sample_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    play_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    album: Mapped[Optional["Album"]] = relationship("Album", back_populates="tracks")
    genres: Mapped[List["Genre"]] = relationship("Genre", secondary=track_genres, back_populates="tracks")
    audio_files: Mapped[List["AudioFile"]] = relationship("AudioFile", back_populates="track", cascade="all, delete-orphan")


class AudioFile(Base):
    """Audio file with specific quality level."""
    __tablename__ = "audio_files"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    track_id: Mapped[str] = mapped_column(String(36), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    quality_level: Mapped[AudioQuality] = mapped_column(SQLEnum(AudioQuality), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    track: Mapped["Track"] = relationship("Track", back_populates="audio_files")


class PlaybackState(Base):
    """User playback state for syncing across devices."""
    __tablename__ = "playback_states"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    current_track_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tracks.id", ondelete="SET NULL"), nullable=True)
    position_seconds: Mapped[int] = mapped_column(Integer, default=0)
    is_playing: Mapped[bool] = mapped_column(default=False)
    shuffle_mode: Mapped[bool] = mapped_column(default=False)
    repeat_mode: Mapped[str] = mapped_column(String(20), default="off")  # off, one, all
    volume: Mapped[float] = mapped_column(default=1.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    current_track: Mapped[Optional["Track"]] = relationship("Track")


class PlayHistory(Base):
    """Track play history for user."""
    __tablename__ = "play_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    track_id: Mapped[str] = mapped_column(String(36), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    played_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    duration_played: Mapped[int] = mapped_column(Integer, default=0)  # seconds

    # Relationships
    track: Mapped["Track"] = relationship("Track")
