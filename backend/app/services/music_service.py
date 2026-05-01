"""Music streaming service for Phase 226."""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.music import Artist, Album, Track, Genre


class MusicService:
    """Service for music content management."""

    @staticmethod
    async def create_artist(db: AsyncSession, name: str, bio: str = None, image_url: str = None) -> Artist:
        artist = Artist(name=name, bio=bio, image_url=image_url)
        db.add(artist)
        await db.commit()
        await db.refresh(artist)
        return artist

    @staticmethod
    async def get_artist(db: AsyncSession, artist_id: str) -> Optional[Artist]:
        result = await db.execute(select(Artist).where(Artist.id == artist_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_artists(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Artist]:
        result = await db.execute(select(Artist).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def delete_artist(db: AsyncSession, artist_id: str) -> bool:
        result = await db.execute(select(Artist).where(Artist.id == artist_id))
        artist = result.scalar_one_or_none()
        if not artist:
            return False
        await db.delete(artist)
        await db.commit()
        return True

    @staticmethod
    async def create_album(db: AsyncSession, artist_id: str, title: str, release_date=None, cover_art_url=None, album_type="album") -> Album:
        album = Album(artist_id=artist_id, title=title, release_date=release_date, cover_art_url=cover_art_url, album_type=album_type)
        db.add(album)
        await db.commit()
        await db.refresh(album)
        return album

    @staticmethod
    async def get_album(db: AsyncSession, album_id: str) -> Optional[Album]:
        result = await db.execute(select(Album).where(Album.id == album_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_albums(db: AsyncSession, artist_id: str = None, skip: int = 0, limit: int = 20) -> List[Album]:
        query = select(Album)
        if artist_id:
            query = query.where(Album.artist_id == artist_id)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def delete_album(db: AsyncSession, album_id: str) -> bool:
        result = await db.execute(select(Album).where(Album.id == album_id))
        album = result.scalar_one_or_none()
        if not album:
            return False
        await db.delete(album)
        await db.commit()
        return True

    @staticmethod
    async def create_track(db: AsyncSession, title: str, album_id: str = None, duration_seconds: int = None, track_number: int = None, disc_number: int = 1, genre_ids: List[str] = None) -> Track:
        track = Track(title=title, album_id=album_id, duration_seconds=duration_seconds, track_number=track_number, disc_number=disc_number)
        if genre_ids:
            result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
            genres = result.scalars().all()
            track.genres = list(genres)
        db.add(track)
        await db.commit()
        await db.refresh(track)
        # Eagerly load genres for response
        result = await db.execute(select(Track).options(selectinload(Track.genres)).where(Track.id == track.id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_track(db: AsyncSession, track_id: str) -> Optional[Track]:
        result = await db.execute(select(Track).options(selectinload(Track.genres)).where(Track.id == track_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_tracks(db: AsyncSession, album_id: str = None, skip: int = 0, limit: int = 20) -> List[Track]:
        query = select(Track).options(selectinload(Track.genres))
        if album_id:
            query = query.where(Track.album_id == album_id)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def delete_track(db: AsyncSession, track_id: str) -> bool:
        result = await db.execute(select(Track).where(Track.id == track_id))
        track = result.scalar_one_or_none()
        if not track:
            return False
        await db.delete(track)
        await db.commit()
        return True

    @staticmethod
    async def create_genre(db: AsyncSession, name: str) -> Genre:
        genre = Genre(name=name)
        db.add(genre)
        await db.commit()
        await db.refresh(genre)
        return genre

    @staticmethod
    async def list_genres(db: AsyncSession) -> List[Genre]:
        result = await db.execute(select(Genre))
        return result.scalars().all()

    @staticmethod
    async def search_music(db: AsyncSession, query: str, skip: int = 0, limit: int = 10) -> dict:
        search_term = f"%{query}%"
        artists_result = await db.execute(select(Artist).where(Artist.name.ilike(search_term)).offset(skip).limit(limit))
        albums_result = await db.execute(select(Album).where(Album.title.ilike(search_term)).offset(skip).limit(limit))
        tracks_result = await db.execute(select(Track).options(selectinload(Track.genres)).where(Track.title.ilike(search_term)).offset(skip).limit(limit))
        return {
            "artists": artists_result.scalars().all(),
            "albums": albums_result.scalars().all(),
            "tracks": tracks_result.scalars().all(),
        }
