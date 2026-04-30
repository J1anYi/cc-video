from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.content_protection import ContentDRM, GeoBlock, DeviceLimit

router = APIRouter(prefix="/protection", tags=["protection"])


class DRMCreate(BaseModel):
    movie_id: int
    drm_type: str
    license_url: str


class GeoBlockCreate(BaseModel):
    movie_id: int
    country_code: str
    is_allowed: bool = False


@router.post("/drm")
async def create_drm(data: DRMCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    drm = ContentDRM(movie_id=data.movie_id, drm_type=data.drm_type, license_url=data.license_url)
    db.add(drm)
    await db.commit()
    return {"id": drm.id, "drm_type": drm.drm_type}


@router.post("/geo-block")
async def create_geo_block(data: GeoBlockCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    block = GeoBlock(movie_id=data.movie_id, country_code=data.country_code, is_allowed=data.is_allowed)
    db.add(block)
    await db.commit()
    return {"id": block.id}


@router.get("/devices")
async def get_devices(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    from sqlalchemy import select
    query = select(DeviceLimit).where(DeviceLimit.user_id == current_user.id)
    result = await db.execute(query)
    devices = result.scalars().all()
    return {"devices": [{"id": d.id, "device_name": d.device_name} for d in devices]}
