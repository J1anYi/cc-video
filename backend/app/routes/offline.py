"""Offline and sync API routes."""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..services.download_manager import DownloadManager
from ..services.sync_service import SyncService
from ..schemas.offline import (
    DownloadRequest, DownloadResponse, DownloadQueueResponse,
    NetworkStatus, WatchProgressSync, PreferenceSync,
    SyncProgress, PreloadSuggestion, OfflineLicense
)

router = APIRouter(prefix="/offline", tags=["offline"])


def get_current_user_id(x_user_id: str = Header(...)) -> int:
    return int(x_user_id)


def get_device_id(x_device_id: str = Header(...)) -> str:
    return x_device_id


@router.post("/downloads", response_model=DownloadResponse)
async def queue_download(
    request: DownloadRequest,
    network_status: NetworkStatus,
    user_id: int = Depends(get_current_user_id),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db)
):
    """Queue a new download for offline viewing."""
    manager = DownloadManager(db)
    try:
        download = await manager.queue_download(user_id, device_id, request, network_status)
        return DownloadResponse(
            id=download.id,
            movie_id=download.movie_id,
            movie_title="",
            quality=download.quality,
            status=download.status.value,
            progress=download.progress,
            file_size=download.file_size,
            downloaded_bytes=download.downloaded_bytes,
            created_at=download.created_at,
            completed_at=download.completed_at,
            expires_at=download.expires_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/downloads", response_model=DownloadQueueResponse)
async def get_downloads(
    user_id: int = Depends(get_current_user_id),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db)
):
    """Get all downloads for current device."""
    manager = DownloadManager(db)
    downloads = await manager.get_user_downloads(user_id, device_id)
    storage = await manager.get_storage_usage(user_id, device_id)

    return DownloadQueueResponse(
        queue=[
            DownloadResponse(
                id=d.id,
                movie_id=d.movie_id,
                movie_title="",
                quality=d.quality,
                status=d.status.value,
                progress=d.progress,
                file_size=d.file_size,
                downloaded_bytes=d.downloaded_bytes,
                created_at=d.created_at,
                completed_at=d.completed_at,
                expires_at=d.expires_at
            )
            for d in downloads
        ],
        active_downloads=sum(1 for d in downloads if d.status.value == "downloading"),
        queued_downloads=sum(1 for d in downloads if d.status.value == "pending"),
        total_storage_bytes=storage["total_storage_bytes"],
        available_storage_bytes=storage["available_storage_bytes"]
    )


@router.post("/downloads/{download_id}/start")
async def start_download(
    download_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Start a queued download."""
    manager = DownloadManager(db)
    download = await manager.start_download(download_id)
    if download:
        return {"status": "started"}
    raise HTTPException(status_code=404, detail="Download not found")


@router.patch("/downloads/{download_id}/progress")
async def update_progress(
    download_id: int,
    progress: float,
    downloaded_bytes: int,
    db: AsyncSession = Depends(get_db)
):
    """Update download progress."""
    manager = DownloadManager(db)
    download = await manager.update_progress(download_id, progress, downloaded_bytes)
    if download:
        return {"progress": download.progress}
    raise HTTPException(status_code=404, detail="Download not found")


@router.post("/downloads/{download_id}/pause")
async def pause_download(
    download_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Pause an active download."""
    manager = DownloadManager(db)
    download = await manager.pause_download(download_id, user_id)
    if download:
        return {"status": "paused"}
    raise HTTPException(status_code=404, detail="Download not found")


@router.post("/downloads/{download_id}/resume")
async def resume_download(
    download_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Resume a paused download."""
    manager = DownloadManager(db)
    download = await manager.resume_download(download_id, user_id)
    if download:
        return {"status": "resumed"}
    raise HTTPException(status_code=404, detail="Download not found")


@router.delete("/downloads/{download_id}")
async def cancel_download(
    download_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Cancel and remove a download."""
    manager = DownloadManager(db)
    if await manager.cancel_download(download_id, user_id):
        return {"status": "cancelled"}
    raise HTTPException(status_code=404, detail="Download not found")


@router.get("/preloads", response_model=List[PreloadSuggestion])
async def get_preload_suggestions(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get suggested content to preload."""
    manager = DownloadManager(db)
    return await manager.get_preload_suggestions(user_id)


@router.get("/licenses/{movie_id}", response_model=OfflineLicense)
async def get_offline_license(
    movie_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get offline playback license for a movie."""
    return OfflineLicense(
        movie_id=movie_id,
        license_key="offline_license_key",
        expires_at=datetime.utcnow() + timedelta(days=30),
        renewal_url="/offline/licenses/{movie_id}/renew"
    )


# Sync endpoints
@router.post("/sync/watch-progress")
async def sync_watch_progress(
    progress_items: List[WatchProgressSync],
    user_id: int = Depends(get_current_user_id),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db)
):
    """Sync watch progress from device."""
    service = SyncService(db)
    return await service.sync_watch_progress(user_id, device_id, progress_items)


@router.get("/sync/watch-progress", response_model=List[WatchProgressSync])
async def get_watch_progress(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get watch progress from all devices."""
    service = SyncService(db)
    return await service.get_watch_progress(user_id)


@router.post("/sync/preferences")
async def sync_preferences(
    preferences: List[PreferenceSync],
    user_id: int = Depends(get_current_user_id),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db)
):
    """Sync user preferences from device."""
    service = SyncService(db)
    return await service.sync_preferences(user_id, device_id, preferences)


@router.get("/sync/status", response_model=SyncProgress)
async def get_sync_status(
    user_id: int = Depends(get_current_user_id),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db)
):
    """Get sync status for device."""
    service = SyncService(db)
    return await service.get_sync_status(user_id, device_id)


@router.post("/sync/full")
async def trigger_full_sync(
    user_id: int = Depends(get_current_user_id),
    device_id: str = Depends(get_device_id),
    db: AsyncSession = Depends(get_db)
):
    """Trigger a full sync."""
    service = SyncService(db)
    return await service.trigger_full_sync(user_id, device_id)
