"""Mobile platform API routes."""
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..database import get_db
from ..services.mobile import MobileService
from ..schemas.mobile import (
    PushTokenCreate, PushTokenResponse, MobileAppConfig,
    MobileDownloadRequest, MobileDownloadStatus, OfflineContentResponse,
    DeviceInfo, PWAManifest
)
from ..models.mobile import PlatformEnum

router = APIRouter(prefix="/mobile", tags=["mobile"])


def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> int:
    """Extract user ID from header."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="User ID required")
    return int(x_user_id)


@router.get("/config", response_model=MobileAppConfig)
async def get_app_config(
    platform: str = "web",
    app_version: str = "1.0.0",
    db: AsyncSession = Depends(get_db)
):
    """Get mobile app configuration."""
    service = MobileService(db)
    try:
        platform_enum = PlatformEnum(platform.lower())
    except ValueError:
        platform_enum = PlatformEnum.WEB
    return service.get_app_config(platform_enum, app_version)


@router.get("/manifest.json")
async def get_pwa_manifest(request: Request, db: AsyncSession = Depends(get_db)):
    """Get PWA manifest for progressive web app."""
    service = MobileService(db)
    base_url = str(request.base_url).rstrip("/")
    return service.get_pwa_manifest(base_url)


@router.post("/push-tokens", response_model=PushTokenResponse)
async def register_push_token(
    token_data: PushTokenCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Register a push notification token."""
    service = MobileService(db)
    token = await service.register_push_token(user_id, token_data)
    return token


@router.delete("/push-tokens/{device_id}")
async def unregister_push_token(
    device_id: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Unregister a push notification token."""
    service = MobileService(db)
    if await service.unregister_push_token(user_id, device_id):
        return {"status": "unregistered"}
    raise HTTPException(status_code=404, detail="Push token not found")


@router.post("/devices")
async def register_device(
    device_info: DeviceInfo,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Register or update device information."""
    service = MobileService(db)
    device = await service.register_device(user_id, device_info.model_dump())
    return {"device_id": device.device_id, "status": "registered"}


@router.get("/devices")
async def list_user_devices(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """List all registered devices for current user."""
    from sqlalchemy import select
    from ..models.mobile import DeviceSession
    query = select(DeviceSession).where(
        DeviceSession.user_id == user_id
    ).order_by(DeviceSession.last_active.desc())
    result = await db.execute(query)
    devices = result.scalars().all()
    return {"devices": [
        {
            "device_id": d.device_id,
            "device_name": d.device_name,
            "platform": d.platform.value,
            "os_version": d.os_version,
            "app_version": d.app_version,
            "last_active": d.last_active.isoformat()
        }
        for d in devices
    ]}


@router.delete("/devices/{device_id}")
async def remove_device(
    device_id: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Remove a registered device."""
    from sqlalchemy import select
    from ..models.mobile import DeviceSession
    query = select(DeviceSession).where(
        DeviceSession.user_id == user_id,
        DeviceSession.device_id == device_id
    )
    result = await db.execute(query)
    device = result.scalar_one_or_none()
    if device:
        await db.delete(device)
        await db.commit()
        return {"status": "removed"}
    raise HTTPException(status_code=404, detail="Device not found")


@router.post("/downloads", response_model=MobileDownloadStatus)
async def create_download(
    download_request: MobileDownloadRequest,
    device_id: str = Header(..., alias="X-Device-ID"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a new download request."""
    service = MobileService(db)
    download = await service.create_download(user_id, device_id, download_request)
    return MobileDownloadStatus(
        id=download.id,
        movie_id=download.movie_id,
        movie_title="",
        quality=download.quality,
        status=download.status.value,
        progress=download.progress,
        file_size=download.file_size,
        downloaded_bytes=download.downloaded_bytes,
        created_at=download.created_at,
        completed_at=download.completed_at
    )


@router.get("/downloads", response_model=OfflineContentResponse)
async def list_downloads(
    device_id: str = Header(..., alias="X-Device-ID"),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """List all downloads for current device."""
    service = MobileService(db)
    downloads = await service.get_user_downloads(user_id, device_id)
    total_storage = sum(d.file_size for d in downloads if d.status.value == "completed")
    return OfflineContentResponse(
        downloads=[
            MobileDownloadStatus(
                id=d.id,
                movie_id=d.movie_id,
                movie_title="",
                quality=d.quality,
                status=d.status.value,
                progress=d.progress,
                file_size=d.file_size,
                downloaded_bytes=d.downloaded_bytes,
                created_at=d.created_at,
                completed_at=d.completed_at
            )
            for d in downloads
        ],
        total_storage_bytes=total_storage,
        max_storage_bytes=10 * 1024 * 1024 * 1024
    )


@router.delete("/downloads/{download_id}")
async def delete_download(
    download_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Delete a download."""
    service = MobileService(db)
    if await service.delete_download(user_id, download_id):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Download not found")
