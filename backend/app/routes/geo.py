"""Geo-restriction API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.geo import GeoRuleType, GeoAction
from app.schemas.geo import (
    GeoConfigCreate, GeoConfigResponse,
    GeoRuleCreate, GeoRuleResponse,
    AccessCheckRequest, AccessCheckResponse,
    VPNDetectionResponse, WhitelistCreate, BlacklistCreate
)
from app.services.geo_service import GeoService
from app.middleware.tenant import get_tenant_id

router = APIRouter(prefix="/geo", tags=["geo"])


@router.post("/config", response_model=GeoConfigResponse)
async def configure_geo(
    config: GeoConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    return await service.configure_geo(
        tenant_id=tenant_id,
        enabled=config.enabled,
        default_action=config.default_action,
        vpn_detection_enabled=config.vpn_detection_enabled,
        vpn_action=config.vpn_action,
        proxy_detection_enabled=config.proxy_detection_enabled,
        proxy_action=config.proxy_action,
        bypass_prevention_enabled=config.bypass_prevention_enabled,
        redirect_url=config.redirect_url,
    )


@router.get("/config", response_model=GeoConfigResponse)
async def get_geo_config(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    config = await service.get_configuration(tenant_id)
    if not config:
        raise HTTPException(status_code=404, detail="Geo configuration not found")
    return config


@router.post("/rules", response_model=GeoRuleResponse)
async def create_geo_rule(
    rule: GeoRuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    return await service.create_rule(
        tenant_id=tenant_id,
        rule_type=rule.rule_type,
        action=rule.action,
        country_code=rule.country_code,
        region_code=rule.region_code,
        content_id=rule.content_id,
        content_type=rule.content_type,
        priority=rule.priority,
        expires_at=rule.expires_at,
    )


@router.get("/rules", response_model=List[GeoRuleResponse])
async def list_geo_rules(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    return await service.list_rules(tenant_id)


@router.post("/check", response_model=AccessCheckResponse)
async def check_geo_access(
    request: AccessCheckRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    allowed, action, country_code, region_code, is_vpn, is_proxy, block_reason = await service.check_access(
        tenant_id=tenant_id,
        ip_address=request.ip_address,
        content_id=request.content_id,
        content_type=request.content_type,
        user_agent=req.headers.get("user-agent"),
        user_id=current_user.id,
    )
    return AccessCheckResponse(
        allowed=allowed,
        action=action,
        country_code=country_code,
        region_code=region_code,
        is_vpn=is_vpn,
        is_proxy=is_proxy,
        block_reason=block_reason,
    )


@router.get("/vpn-detect/{ip_address}", response_model=VPNDetectionResponse)
async def detect_vpn(
    ip_address: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    detection = await service.detect_vpn(tenant_id, ip_address)
    return VPNDetectionResponse(
        ip_address=detection.ip_address,
        is_vpn=detection.is_vpn,
        is_proxy=detection.is_proxy,
        is_tor=detection.is_tor,
        confidence_score=detection.confidence_score,
        provider_name=detection.provider_name,
    )


@router.post("/whitelist")
async def add_whitelist(
    request: WhitelistCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    entry = await service.add_whitelist(
        tenant_id=tenant_id,
        country_code=request.country_code,
        region_code=request.region_code,
        content_id=request.content_id,
        content_type=request.content_type,
        notes=request.notes,
    )
    return {"id": entry.id, "country_code": entry.country_code}


@router.post("/blacklist")
async def add_blacklist(
    request: BlacklistCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = GeoService(db)
    entry = await service.add_blacklist(
        tenant_id=tenant_id,
        country_code=request.country_code,
        region_code=request.region_code,
        content_id=request.content_id,
        content_type=request.content_type,
        reason=request.reason,
    )
    return {"id": entry.id, "country_code": entry.country_code}
