from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.mobile import OfflineDownload, PushNotification

router = APIRouter(prefix="/mobile", tags=["mobile"])


class DownloadCreate(BaseModel):
    movie_id: int
    quality: str = "high"


class PushRegister(BaseModel):
    device_token: str
    platform: str


@router.post("/downloads")
async def create_download(data: DownloadCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    download = OfflineDownload(user_id=current_user.id, movie_id=data.movie_id, quality=data.quality)
    db.add(download)
    await db.commit()
    return {"id": download.id, "status": download.status}


@router.get("/downloads")
async def get_downloads(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    from sqlalchemy import select
    query = select(OfflineDownload).where(OfflineDownload.user_id == current_user.id)
    result = await db.execute(query)
    downloads = result.scalars().all()
    return {"downloads": [{"id": d.id, "movie_id": d.movie_id, "status": d.status, "progress": d.progress} for d in downloads]}


@router.post("/push/register")
async def register_push(data: PushRegister, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    push = PushNotification(user_id=current_user.id, device_token=data.device_token, platform=data.platform)
    db.add(push)
    await db.commit()
    return {"id": push.id, "platform": push.platform}
