"""Geo-restriction models."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class GeoRuleType(enum.Enum):
    ALLOW = "allow"
    BLOCK = "block"


class GeoAction(enum.Enum):
    ALLOW = "allow"
    BLOCK = "block"
    REDIRECT = "redirect"


class DetectionMethod(enum.Enum):
    IP_LOOKUP = "ip_lookup"
    VPN_DATABASE = "vpn_database"
    BEHAVIORAL = "behavioral"


class GeoConfiguration(Base):
    """Geo-restriction configuration per tenant."""
    __tablename__ = "geo_configurations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    default_action: Mapped[GeoAction] = mapped_column(SQLEnum(GeoAction), default=GeoAction.BLOCK)
    
    vpn_detection_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    vpn_action: Mapped[GeoAction] = mapped_column(SQLEnum(GeoAction), default=GeoAction.BLOCK)
    
    proxy_detection_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    proxy_action: Mapped[GeoAction] = mapped_column(SQLEnum(GeoAction), default=GeoAction.BLOCK)
    
    bypass_prevention_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    redirect_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GeoRule(Base):
    """Geographic access rule."""
    __tablename__ = "geo_rules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    content_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    content_type: Mapped[str] = mapped_column(String(50), default="all")
    
    rule_type: Mapped[GeoRuleType] = mapped_column(SQLEnum(GeoRuleType), nullable=False)
    
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, index=True)
    region_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    action: Mapped[GeoAction] = mapped_column(SQLEnum(GeoAction), default=GeoAction.BLOCK)
    
    priority: Mapped[int] = mapped_column(Integer, default=0)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class GeoWhitelist(Base):
    """Whitelisted regions."""
    __tablename__ = "geo_whitelists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    country_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    region_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    content_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), default="all")
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GeoBlacklist(Base):
    """Blacklisted regions."""
    __tablename__ = "geo_blacklists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    country_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    region_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    content_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), default="all")
    
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class VPNDetection(Base):
    """VPN/proxy detection record."""
    __tablename__ = "vpn_detections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    is_vpn: Mapped[bool] = mapped_column(Boolean, default=False)
    is_proxy: Mapped[bool] = mapped_column(Boolean, default=False)
    is_tor: Mapped[bool] = mapped_column(Boolean, default=False)
    
    detection_method: Mapped[DetectionMethod] = mapped_column(SQLEnum(DetectionMethod), default=DetectionMethod.IP_LOOKUP)
    
    confidence_score: Mapped[float] = mapped_column(default=0.0)
    
    provider_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class GeoAccessLog(Base):
    """Access attempt log."""
    __tablename__ = "geo_access_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    region_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    content_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str] = mapped_column(String(50), default="all")
    
    action_taken: Mapped[GeoAction] = mapped_column(SQLEnum(GeoAction), nullable=False)
    
    was_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    block_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
