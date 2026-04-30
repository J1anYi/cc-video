"""Mobile platform service for CC Video API."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ..models.mobile import PushToken, MobileDownload, DeviceSession, PlatformEnum, DownloadStatus
from ..schemas.mobile import (
    PushTokenCreate, PushTokenResponse, MobileAppConfig,
    MobileDownloadRequest, MobileDownloadStatus, OfflineContentResponse
)


class MobileService:
    """Service for mobile platform operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # Push Token Management
    async def register_push_token(self, user_id: int, token_data: PushTokenCreate) -> PushToken:
        """Register or update a push notification token."""
        query = select(PushToken).where(
            PushToken.user_id == user_id,
            PushToken.device_id == token_data.device_id
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            existing.push_token = token_data.push_token
            existing.is_active = True
            existing.updated_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        push_token = PushToken(
            user_id=user_id,
            device_id=token_data.device_id,
            platform=PlatformEnum(token_data.platform.value),
            push_token=token_data.push_token
        )
        self.db.add(push_token)
        await self.db.commit()
        await self.db.refresh(push_token)
        return push_token

    async def unregister_push_token(self, user_id: int, device_id: str) -> bool:
        """Deactivate a push token."""
        query = select(PushToken).where(
            PushToken.user_id == user_id,
            PushToken.device_id == device_id
        )
        result = await self.db.execute(query)
        token = result.scalar_one_or_none()

        if token:
            token.is_active = False
            await self.db.commit()
            return True
        return False

    # Device Session Management
    async def register_device(self, user_id: int, device_info: Dict[str, Any]) -> DeviceSession:
        """Register or update device session."""
        query = select(DeviceSession).where(
            DeviceSession.user_id == user_id,
            DeviceSession.device_id == device_info["device_id"]
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            existing.device_name = device_info.get("device_name")
            existing.os_version = device_info.get("os_version")
            existing.app_version = device_info.get("app_version")
            existing.last_active = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        device = DeviceSession(
            user_id=user_id,
            device_id=device_info["device_id"],
            device_name=device_info.get("device_name"),
            platform=PlatformEnum(device_info["platform"].value),
            os_version=device_info.get("os_version"),
            app_version=device_info.get("app_version")
        )
        self.db.add(device)
        await self.db.commit()
        await self.db.refresh(device)
        return device

    # Download Management
    async def create_download(
        self, user_id: int, device_id: str, download_request: MobileDownloadRequest
    ) -> MobileDownload:
        """Create a new download request."""
        download = MobileDownload(
            user_id=user_id,
            movie_id=download_request.movie_id,
            device_id=device_id,
            quality=download_request.quality
        )
        self.db.add(download)
        await self.db.commit()
        await self.db.refresh(download)
        return download

    async def update_download_progress(
        self, download_id: int, progress: float, downloaded_bytes: int
    ) -> Optional[MobileDownload]:
        """Update download progress."""
        query = select(MobileDownload).where(MobileDownload.id == download_id)
        result = await self.db.execute(query)
        download = result.scalar_one_or_none()

        if download:
            download.progress = progress
            download.downloaded_bytes = downloaded_bytes
            if progress >= 100:
                download.status = DownloadStatus.COMPLETED
                download.completed_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(download)
        return download

    async def get_user_downloads(self, user_id: int, device_id: str) -> List[MobileDownload]:
        """Get all downloads for a user on a device."""
        query = select(MobileDownload).where(
            MobileDownload.user_id == user_id,
            MobileDownload.device_id == device_id
        ).order_by(MobileDownload.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_download(self, user_id: int, download_id: int) -> bool:
        """Delete a download."""
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

    # App Configuration
    def get_app_config(self, platform: PlatformEnum, app_version: str) -> MobileAppConfig:
        """Get mobile app configuration."""
        config = MobileAppConfig(
            min_app_version="1.0.0",
            latest_app_version="1.2.0",
            force_update=False,
            maintenance_mode=False,
            feature_flags={
                "offline_mode": True,
                "picture_in_picture": True,
                "background_playback": True,
                "download_quality_selection": True,
                "cellular_downloads": False,
            }
        )
        return config

    # PWA Manifest
    def get_pwa_manifest(self, base_url: str) -> Dict[str, Any]:
        """Generate PWA manifest."""
        return {
            "name": "CC Video",
            "short_name": "CC Video",
            "description": "Watch movies anytime, anywhere",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#000000",
            "theme_color": "#e50914",
            "icons": [
                {
                    "src": f"{base_url}/icons/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": f"{base_url}/icons/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                },
                {
                    "src": f"{base_url}/icons/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "maskable"
                }
            ],
            "categories": ["entertainment", "video"],
            "shortcuts": [
                {
                    "name": "Continue Watching",
                    "url": "/continue-watching",
                    "icons": [{"src": f"{base_url}/icons/play.png", "sizes": "96x96"}]
                },
                {
                    "name": "My Downloads",
                    "url": "/downloads",
                    "icons": [{"src": f"{base_url}/icons/download.png", "sizes": "96x96"}]
                }
            ]
        }
