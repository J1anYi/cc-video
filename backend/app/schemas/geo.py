"""Geo-restriction schemas for API validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.geo import GeoRuleType, GeoAction, DetectionMethod


class GeoConfigCreate(BaseModel):
    enabled: bool = True
    default_action: GeoAction = GeoAction.BLOCK
    vpn_detection_enabled: bool = False
    vpn_action: GeoAction = GeoAction.BLOCK
    proxy_detection_enabled: bool = False
    proxy_action: GeoAction = GeoAction.BLOCK
    bypass_prevention_enabled: bool = True
    redirect_url: Optional[str] = None


class GeoConfigResponse(BaseModel):
    id: int
    tenant_id: int
    enabled: bool
    default_action: GeoAction
    vpn_detection_enabled: bool
    proxy_detection_enabled: bool
    bypass_prevention_enabled: bool
    redirect_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class GeoRuleCreate(BaseModel):
    content_id: Optional[int] = None
    content_type: str = "all"
    rule_type: GeoRuleType
    country_code: Optional[str] = None
    region_code: Optional[str] = None
    action: GeoAction = GeoAction.BLOCK
    priority: int = 0
    expires_at: Optional[datetime] = None


class GeoRuleResponse(BaseModel):
    id: int
    content_id: Optional[int]
    content_type: str
    rule_type: GeoRuleType
    country_code: Optional[str]
    region_code: Optional[str]
    action: GeoAction
    priority: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AccessCheckRequest(BaseModel):
    ip_address: str
    content_id: Optional[int] = None
    content_type: str = "all"


class AccessCheckResponse(BaseModel):
    allowed: bool
    action: GeoAction
    country_code: Optional[str]
    region_code: Optional[str]
    is_vpn: bool
    is_proxy: bool
    block_reason: Optional[str]


class VPNDetectionResponse(BaseModel):
    ip_address: str
    is_vpn: bool
    is_proxy: bool
    is_tor: bool
    confidence_score: float
    provider_name: Optional[str]


class WhitelistCreate(BaseModel):
    country_code: str
    region_code: Optional[str] = None
    content_id: Optional[int] = None
    content_type: str = "all"
    notes: Optional[str] = None


class BlacklistCreate(BaseModel):
    country_code: str
    region_code: Optional[str] = None
    content_id: Optional[int] = None
    content_type: str = "all"
    reason: Optional[str] = None
