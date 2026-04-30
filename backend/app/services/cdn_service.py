"""CDN service layer."""
import uuid
import json
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cdn import (
    CDNConfiguration,
    CDNCacheRule,
    CacheInvalidation,
    CDNMetrics,
    CDNProvider,
    CacheBehavior,
    InvalidationStatus,
)
from app.schemas.cdn import (
    CDNConfigCreate,
    CacheRuleCreate,
    InvalidationRequest,
)


class CDNService:
    """Service for CDN operations."""

    async def configure(self, db: AsyncSession, tenant_id: int, config_data: CDNConfigCreate) -> CDNConfiguration:
        existing = await db.execute(
            select(CDNConfiguration).where(
                CDNConfiguration.tenant_id == tenant_id,
                CDNConfiguration.is_active == True,
            )
        )
        existing_config = existing.scalar_one_or_none()
        if existing_config:
            existing_config.provider = config_data.provider
            existing_config.distribution_id = config_data.distribution_id
            existing_config.domain_name = config_data.domain_name
            existing_config.origin_url = config_data.origin_url
            existing_config.default_ttl = config_data.default_ttl
            existing_config.max_ttl = config_data.max_ttl
            existing_config.https_enabled = config_data.https_enabled
            existing_config.compression_enabled = config_data.compression_enabled
            existing_config.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(existing_config)
            return existing_config

        config = CDNConfiguration(
            tenant_id=tenant_id, provider=config_data.provider,
            distribution_id=config_data.distribution_id, domain_name=config_data.domain_name,
            origin_url=config_data.origin_url, default_ttl=config_data.default_ttl,
            max_ttl=config_data.max_ttl, https_enabled=config_data.https_enabled,
            compression_enabled=config_data.compression_enabled,
        )
        db.add(config)
        await db.commit()
        await db.refresh(config)
        return config

    async def get_config(self, db: AsyncSession, tenant_id: int) -> Optional[CDNConfiguration]:
        result = await db.execute(
            select(CDNConfiguration).where(
                CDNConfiguration.tenant_id == tenant_id,
                CDNConfiguration.is_active == True,
            )
        )
        return result.scalar_one_or_none()

    async def create_cache_rule(self, db: AsyncSession, tenant_id: int, rule_data: CacheRuleCreate) -> CDNCacheRule:
        rule = CDNCacheRule(
            tenant_id=tenant_id, path_pattern=rule_data.path_pattern,
            content_type=rule_data.content_type, behavior=rule_data.behavior,
            ttl=rule_data.ttl, query_string_whitelist=rule_data.query_string_whitelist,
            priority=rule_data.priority,
        )
        db.add(rule)
        await db.commit()
        await db.refresh(rule)
        return rule

    async def get_cache_rules(self, db: AsyncSession, tenant_id: int) -> List[CDNCacheRule]:
        result = await db.execute(
            select(CDNCacheRule)
            .where(CDNCacheRule.tenant_id == tenant_id, CDNCacheRule.is_active == True)
            .order_by(CDNCacheRule.priority.desc())
        )
        return list(result.scalars().all())

    async def delete_cache_rule(self, db: AsyncSession, tenant_id: int, rule_id: int) -> bool:
        result = await db.execute(
            select(CDNCacheRule).where(CDNCacheRule.id == rule_id, CDNCacheRule.tenant_id == tenant_id)
        )
        rule = result.scalar_one_or_none()
        if rule:
            rule.is_active = False
            await db.commit()
            return True
        return False

    async def invalidate_cache(self, db: AsyncSession, tenant_id: int, invalidation_data: InvalidationRequest) -> CacheInvalidation:
        invalidation_id = str(uuid.uuid4())
        invalidation = CacheInvalidation(
            tenant_id=tenant_id, invalidation_id=invalidation_id,
            paths=json.dumps(invalidation_data.paths), status=InvalidationStatus.PENDING,
        )
        db.add(invalidation)
        await db.commit()
        await db.refresh(invalidation)
        invalidation.status = InvalidationStatus.COMPLETED
        invalidation.completed_at = datetime.utcnow()
        await db.commit()
        await db.refresh(invalidation)
        return invalidation

    async def get_invalidation_status(self, db: AsyncSession, tenant_id: int, invalidation_id: str) -> Optional[CacheInvalidation]:
        result = await db.execute(
            select(CacheInvalidation).where(
                CacheInvalidation.invalidation_id == invalidation_id,
                CacheInvalidation.tenant_id == tenant_id,
            )
        )
        return result.scalar_one_or_none()

    async def record_metrics(self, db: AsyncSession, tenant_id: int, requests: int, hits: int, misses: int, bandwidth_bytes: int, bytes_saved: int, avg_latency_ms: float, error_rate: float) -> CDNMetrics:
        metrics = CDNMetrics(
            tenant_id=tenant_id, requests=requests, hits=hits, misses=misses,
            bandwidth_bytes=bandwidth_bytes, bytes_saved=bytes_saved,
            avg_latency_ms=avg_latency_ms, error_rate=error_rate,
        )
        db.add(metrics)
        await db.commit()
        await db.refresh(metrics)
        return metrics

    async def get_metrics(self, db: AsyncSession, tenant_id: int, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> List[CDNMetrics]:
        if not start_time:
            start_time = datetime.utcnow() - timedelta(days=7)
        if not end_time:
            end_time = datetime.utcnow()
        result = await db.execute(
            select(CDNMetrics).where(
                CDNMetrics.tenant_id == tenant_id,
                CDNMetrics.timestamp >= start_time,
                CDNMetrics.timestamp <= end_time,
            ).order_by(CDNMetrics.timestamp.desc())
        )
        return list(result.scalars().all())

    async def get_metrics_summary(self, db: AsyncSession, tenant_id: int, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> dict:
        if not start_time:
            start_time = datetime.utcnow() - timedelta(days=7)
        if not end_time:
            end_time = datetime.utcnow()
        result = await db.execute(
            select(
                func.sum(CDNMetrics.requests).label("total_requests"),
                func.sum(CDNMetrics.hits).label("total_hits"),
                func.sum(CDNMetrics.misses).label("total_misses"),
                func.sum(CDNMetrics.bandwidth_bytes).label("total_bandwidth"),
                func.sum(CDNMetrics.bytes_saved).label("total_bytes_saved"),
                func.avg(CDNMetrics.avg_latency_ms).label("avg_latency"),
                func.avg(CDNMetrics.error_rate).label("avg_error_rate"),
            ).where(
                CDNMetrics.tenant_id == tenant_id,
                CDNMetrics.timestamp >= start_time,
                CDNMetrics.timestamp <= end_time,
            )
        )
        row = result.one()
        total_requests = row.total_requests or 0
        total_hits = row.total_hits or 0
        hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
        return {
            "total_requests": total_requests, "total_hits": total_hits,
            "total_misses": row.total_misses or 0, "total_bandwidth": row.total_bandwidth or 0,
            "total_bytes_saved": row.total_bytes_saved or 0, "avg_latency_ms": float(row.avg_latency or 0),
            "avg_error_rate": float(row.avg_error_rate or 0), "hit_rate": hit_rate,
        }


cdn_service = CDNService()
