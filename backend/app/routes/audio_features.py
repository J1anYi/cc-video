from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.audio_features import AudioTrackFeature as AudioTrack, AudioEqualizer

router = APIRouter(prefix="/audio", tags=["audio"])


class TrackCreate(BaseModel):
    movie_id: int
    language: str
    title: str
    url: str


@router.post("/tracks")
async def create_track(data: TrackCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    track = AudioTrack(movie_id=data.movie_id, language=data.language, title=data.title, url=data.url)
    db.add(track)
    await db.commit()
    return {"id": track.id, "language": track.language}


@router.get("/tracks/{movie_id}")
async def get_tracks(movie_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    query = select(AudioTrack).where(AudioTrack.movie_id == movie_id)
    result = await db.execute(query)
    tracks = result.scalars().all()
    return {"tracks": [{"id": t.id, "language": t.language, "title": t.title} for t in tracks]}


@router.post("/equalizer")
async def create_equalizer(preset: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    eq = AudioEqualizer(user_id=current_user.id, name=preset, preset=preset)
    db.add(eq)
    await db.commit()
    return {"id": eq.id, "preset": eq.preset}
