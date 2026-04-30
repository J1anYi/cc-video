"""CDN models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class CDNProvider(enum.Enum):
    CLOUDFRONT = "cloudfront"
    FASTLY = "fastly"
    CLOUDFLARE = "cloudflare"
    AKAMAI = "akamai"


class CacheBehavior(enum.Enum):
    CACHE = "cache"
    BYPASS = "bypass"
    NO_CACHE = "no_cache"


class InvalidationStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class CDNConfiguration(Base):
    """CDN configuration per tenant."""
    __tablename__ = "cdn_configurations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    provider: Mapped[CDNProvider] = mapped_column(SQLEnum(CDNProvider), nullable=False)
    
    distribution_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    domain_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    origin_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    default_ttl: Mapped[int] = mapped_column(Integer, default=86400)
    max_ttl: Mapped[int] = mapped_column(Integer, default=31536000)
    
    https_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    compression_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CDNCacheRule(Base):
    """Cache rule configuration."""
    __tablename__ = "cdn_cache_rules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    path_pattern: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    behavior: Mapped[CacheBehavior] = mapped_column(SQLEnum(CacheBehavior), default=CacheBehavior.CACHE)
    
    ttl: Mapped[int] = mapped_column(Integer, default=86400)
    
    query_string_whitelist: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    priority: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CacheInvalidation(Base):
    """Cache invalidation record."""
    __tablename__ = "cache_invalidations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    invalidation_id: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    
    paths: Mapped[str] = mapped_column(Text, nullable=False)
    
    status: Mapped[InvalidationStatus] = mapped_column(SQLEnum(InvalidationStatus), default=InvalidationStatus.PENDING)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class CDNMetrics(Base):
    """CDN performance metrics."""
    __tablename__ = "cdn_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    requests: Mapped[int] = mapped_column(Integer, default=0)
    hits: Mapped[int] = mapped_column(Integer, default=0)
    misses: Mapped[int] = mapped_column(Integer, default=0)
    
    bandwidth_bytes: Mapped[int] = mapped_column(Integer, default=0)
    bytes_saved: Mapped[int] = mapped_column(Integer, default=0)
    
    avg_latency_ms: Mapped[float] = mapped_column(default=0.0)
    
    error_rate: Mapped[float] = mapped_column(default=0.0)
