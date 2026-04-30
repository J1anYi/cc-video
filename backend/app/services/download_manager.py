"""Download manager service for offline content."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
from ..models.mobile import MobileDownload, DownloadStatus
from ..schemas.offline import (
    DownloadRequest, DownloadResponse, DownloadQuality,
    NetworkType, NetworkStatus, PreloadSuggestion
)


class DownloadManager:
    """Manages offline download operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def queue_download(
        self,
        user_id: int,
        device_id: str,
        request: DownloadRequest,
        network_status: NetworkStatus
    ) -> MobileDownload:
        """Queue a new download."""
        if request.wifi_only and not network_status.is_wifi:
            raise ValueError("Wi-Fi required for this download")

        file_sizes = {
            DownloadQuality.Q360P: 300 * 1024 * 1024,
            DownloadQuality.Q480P: 500 * 1024 * 1024,
            DownloadQuality.Q720P: 1000 * 1024 * 1024,
            DownloadQuality.Q1080P: 2500 * 1024 * 1024,
        }

        download = MobileDownload(
            user_id=user_id,
            movie_id=request.movie_id,
            device_id=device_id,
            quality=request.quality.value,
            status=DownloadStatus.PENDING,
            file_size=file_sizes.get(request.quality, 1000 * 1024 * 1024),
            storage_path=f"downloads/{request.movie_id}/{request.quality.value}/{uuid.uuid4()}.mp4",
            expires_at=datetime.utcnow() + timedelta(days=30)
        )

        self.db.add(download)
        await self.db.commit()
        await self.db.refresh(download)
        return download

    async def start_download(self, download_id: int) -> Optional[MobileDownload]:
        query = select(MobileDownload).where(MobileDownload.id == download_id)
        result = await self.db.execute(query)
        download = result.scalar_one_or_none()

        if download and download.status == DownloadStatus.PENDING:
            download.status = DownloadStatus.DOWNLOADING
            await self.db.commit()
            await self.db.refresh(download)
        return download

    async def update_progress(
        self,
        download_id: int,
        progress: float,
        downloaded_bytes: int
    ) -> Optional[MobileDownload]:
        query = select(MobileDownload).where(MobileDownload.id == download_id)
        result = await self.db.execute(query)
        download = result.scalar_one_or_none()

        if download:
            download.progress = min(progress, 100.0)
            download.downloaded_bytes = downloaded_bytes
            if progress >= 100:
                download.status = DownloadStatus.COMPLETED
                download.completed_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(download)
        return download

    async def pause_download(self, download_id: int, user_id: int) -> Optional[MobileDownload]:
        query = select(MobileDownload).where(
            MobileDownload.id == download_id,
            MobileDownload.user_id == user_id
        )
        result = await self.db.execute(query)
        download = result.scalar_one_or_none()

        if download and download.status == DownloadStatus.DOWNLOADING:
            download.status = DownloadStatus.PAUSED
            await self.db.commit()
            await self.db.refresh(download)
        return download

    async def resume_download(self, download_id: int, user_id: int) -> Optional[MobileDownload]:
        query = select(MobileDownload).where(
            MobileDownload.id == download_id,
            MobileDownload.user_id == user_id
        )
        result = await self.db.execute(query)
        download = result.scalar_one_or_none()

        if download and download.status == DownloadStatus.PAUSED:
            download.status = DownloadStatus.PENDING
            await self.db.commit()
            await self.db.refresh(download)
        return download

    async def cancel_download(self, download_id: int, user_id: int) -> bool:
        query = select(MobileDownload).where(
            MobileDownload.id == download_id,
            MobileDownload.user_id == user_id
        )
        result = await self.db.execute(query)
        download = result.scalar_one_or_none()

        if download:
            await self.db.delete(download)
            await self.db.commit()
            return True
        return False

    async def get_user_downloads(self, user_id: int, device_id: str) -> List[MobileDownload]:
        query = select(MobileDownload).where(
            MobileDownload.user_id == user_id,
            MobileDownload.device_id == device_id
        ).order_by(MobileDownload.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_storage_usage(self, user_id: int, device_id: str) -> Dict[str, int]:
        query = select(MobileDownload).where(
            MobileDownload.user_id == user_id,
            MobileDownload.device_id == device_id,
            MobileDownload.status == DownloadStatus.COMPLETED
        )
        result = await self.db.execute(query)
        downloads = result.scalars().all()

        total = sum(d.file_size for d in downloads)
        max_storage = 10 * 1024 * 1024 * 1024

        return {
            "total_storage_bytes": total,
            "available_storage_bytes": max_storage - total,
            "max_storage_bytes": max_storage
        }

    async def get_preload_suggestions(self, user_id: int) -> List[PreloadSuggestion]:
        return []

    async def cleanup_expired_downloads(self) -> int:
        query = select(MobileDownload).where(
            MobileDownload.expires_at < datetime.utcnow()
        )
        result = await self.db.execute(query)
        expired = result.scalars().all()

        count = len(expired)
        for download in expired:
            await self.db.delete(download)

        await self.db.commit()
        return count
