"""CDN schemas."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.cdn import CDNProvider, CacheBehavior, InvalidationStatus


class CDNConfigCreate(BaseModel):
    provider: CDNProvider
    distribution_id: Optional[str] = None
    domain_name: Optional[str] = None
    origin_url: str
    default_ttl: int = 86400
    max_ttl: int = 31536000
    https_enabled: bool = True
    compression_enabled: bool = True


class CDNConfigResponse(BaseModel):
    id: int
    tenant_id: int
    provider: CDNProvider
    distribution_id: Optional[str]
    domain_name: Optional[str]
    origin_url: str
    default_ttl: int
    https_enabled: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CacheRuleCreate(BaseModel):
    path_pattern: str
    content_type: Optional[str] = None
    behavior: CacheBehavior = CacheBehavior.CACHE
    ttl: int = 86400
    query_string_whitelist: Optional[str] = None
    priority: int = 0


class CacheRuleResponse(BaseModel):
    id: int
    path_pattern: str
    behavior: CacheBehavior
    ttl: int
    priority: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InvalidationRequest(BaseModel):
    paths: List[str]


class InvalidationResponse(BaseModel):
    invalidation_id: str
    status: InvalidationStatus
    paths: str
    created_at: datetime


class CDNMetricsResponse(BaseModel):
    timestamp: datetime
    requests: int
    hits: int
    misses: int
    bandwidth_bytes: int
    bytes_saved: int
    avg_latency_ms: float
    hit_rate: float
