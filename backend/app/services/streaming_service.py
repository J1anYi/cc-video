"""Adaptive streaming service."""
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.streaming import (
    AdaptiveStreamVariant,
    BandwidthMetric,
    QualityPreference,
    QualityLevel,
)


class StreamingService:
    """Service for adaptive streaming operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_stream_variant(
        self,
        movie_id: int,
        tenant_id: int,
        quality: QualityLevel,
        resolution: str,
        bitrate: int,
        hls_url: str,
        manifest_url: str = None,
        file_size: int = 0,
    ) -> AdaptiveStreamVariant:
        """Create a stream variant for a movie."""
        variant = AdaptiveStreamVariant(
            movie_id=movie_id,
            tenant_id=tenant_id,
            quality=quality,
            resolution=resolution,
            bitrate=bitrate,
            hls_url=hls_url,
            manifest_url=manifest_url,
            file_size=file_size,
        )
        self.db.add(variant)
        await self.db.commit()
        await self.db.refresh(variant)
        return variant

    async def get_variants_for_movie(
        self, movie_id: int, tenant_id: int
    ) -> List[AdaptiveStreamVariant]:
        """Get all stream variants for a movie."""
        query = select(AdaptiveStreamVariant).where(
            AdaptiveStreamVariant.movie_id == movie_id,
            AdaptiveStreamVariant.tenant_id == tenant_id,
        ).order_by(AdaptiveStreamVariant.bitrate.asc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def record_bandwidth_metric(
        self,
        tenant_id: int,
        bandwidth_kbps: int,
        quality_selected: QualityLevel = None,
        quality_played: QualityLevel = None,
        user_id: int = None,
        movie_id: int = None,
        buffer_events: int = 0,
        rebuffer_time_ms: int = 0,
    ) -> BandwidthMetric:
        """Record bandwidth measurement."""
        metric = BandwidthMetric(
            user_id=user_id,
            tenant_id=tenant_id,
            movie_id=movie_id,
            bandwidth_kbps=bandwidth_kbps,
            quality_selected=quality_selected,
            quality_played=quality_played,
            buffer_events=buffer_events,
            rebuffer_time_ms=rebuffer_time_ms,
        )
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        return metric

    async def get_recommended_quality(
        self, bandwidth_kbps: int
    ) -> QualityLevel:
        """Get recommended quality based on bandwidth."""
        if bandwidth_kbps >= 25000:
            return QualityLevel.ULTRA
        elif bandwidth_kbps >= 8000:
            return QualityLevel.HIGH
        elif bandwidth_kbps >= 4000:
            return QualityLevel.MEDIUM
        else:
            return QualityLevel.LOW

    async def get_bandwidth_stats(
        self,
        tenant_id: int,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> dict:
        """Get bandwidth statistics for a tenant."""
        query = select(BandwidthMetric).where(
            BandwidthMetric.tenant_id == tenant_id,
        )
        
        if start_date:
            query = query.where(BandwidthMetric.created_at >= start_date)
        if end_date:
            query = query.where(BandwidthMetric.created_at <= end_date)
        
        result = await self.db.execute(query)
        metrics = result.scalars().all()
        
        if not metrics:
            return {
                "avg_bandwidth_kbps": 0,
                "total_measurements": 0,
                "avg_buffer_events": 0,
                "avg_rebuffer_time_ms": 0,
            }
        
        return {
            "avg_bandwidth_kbps": sum(m.bandwidth_kbps for m in metrics) // len(metrics),
            "total_measurements": len(metrics),
            "avg_buffer_events": sum(m.buffer_events for m in metrics) // len(metrics),
            "avg_rebuffer_time_ms": sum(m.rebuffer_time_ms for m in metrics) // len(metrics),
        }

    async def set_quality_preference(
        self,
        user_id: int,
        tenant_id: int,
        preferred_quality: QualityLevel,
        auto_adjust: bool = True,
        limit_mobile_data: bool = False,
    ) -> QualityPreference:
        """Set user quality preference."""
        query = select(QualityPreference).where(
            QualityPreference.user_id == user_id,
        )
        result = await self.db.execute(query)
        pref = result.scalar_one_or_none()
        
        if pref:
            pref.preferred_quality = preferred_quality
            pref.auto_adjust = auto_adjust
            pref.limit_mobile_data = limit_mobile_data
            pref.updated_at = datetime.utcnow()
        else:
            pref = QualityPreference(
                user_id=user_id,
                tenant_id=tenant_id,
                preferred_quality=preferred_quality,
                auto_adjust=auto_adjust,
                limit_mobile_data=limit_mobile_data,
            )
            self.db.add(pref)
        
        await self.db.commit()
        await self.db.refresh(pref)
        return pref

    async def get_quality_preference(self, user_id: int) -> Optional[QualityPreference]:
        """Get user quality preference."""
        query = select(QualityPreference).where(
            QualityPreference.user_id == user_id,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
