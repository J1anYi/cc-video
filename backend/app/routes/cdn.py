"""CDN routes."""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.tenant import get_tenant_id
from app.services.cdn_service import cdn_service
from app.schemas.cdn import (
    CDNConfigCreate,
    CDNConfigResponse,
    CacheRuleCreate,
    CacheRuleResponse,
    InvalidationRequest,
    InvalidationResponse,
    CDNMetricsResponse,
)


router = APIRouter(prefix="/cdn", tags=["cdn"])


@router.post("/configure", response_model=CDNConfigResponse)
async def configure_cdn(
    config_data: CDNConfigCreate,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Configure CDN for tenant."""
    config = await cdn_service.configure(db, tenant_id, config_data)
    return config


@router.get("/config", response_model=Optional[CDNConfigResponse])
async def get_cdn_config(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get CDN configuration."""
    config = await cdn_service.get_config(db, tenant_id)
    return config


@router.post("/cache-rules", response_model=CacheRuleResponse)
async def create_cache_rule(
    rule_data: CacheRuleCreate,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Create a cache rule."""
    rule = await cdn_service.create_cache_rule(db, tenant_id, rule_data)
    return rule


@router.get("/cache-rules", response_model=list[CacheRuleResponse])
async def get_cache_rules(
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get all cache rules."""
    rules = await cdn_service.get_cache_rules(db, tenant_id)
    return rules


@router.delete("/cache-rules/{rule_id}")
async def delete_cache_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Delete a cache rule."""
    success = await cdn_service.delete_cache_rule(db, tenant_id, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cache rule not found")
    return {"success": True}


@router.post("/invalidate", response_model=InvalidationResponse)
async def invalidate_cache(
    invalidation_data: InvalidationRequest,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Invalidate CDN cache."""
    invalidation = await cdn_service.invalidate_cache(db, tenant_id, invalidation_data)
    return invalidation


@router.get("/invalidate/{invalidation_id}", response_model=Optional[InvalidationResponse])
async def get_invalidation_status(
    invalidation_id: str,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get invalidation status."""
    invalidation = await cdn_service.get_invalidation_status(db, tenant_id, invalidation_id)
    if not invalidation:
        raise HTTPException(status_code=404, detail="Invalidation not found")
    return invalidation


@router.get("/metrics", response_model=list[CDNMetricsResponse])
async def get_cdn_metrics(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get CDN metrics."""
    metrics = await cdn_service.get_metrics(db, tenant_id, start_time, end_time)
    return metrics


@router.get("/metrics/summary")
async def get_cdn_metrics_summary(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get aggregated CDN metrics."""
    summary = await cdn_service.get_metrics_summary(db, tenant_id, start_time, end_time)
    return summary
