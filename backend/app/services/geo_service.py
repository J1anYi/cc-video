"""Geo-restriction service."""
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib

from app.models.geo import (
    GeoConfiguration, GeoRule, GeoWhitelist, GeoBlacklist, VPNDetection, GeoAccessLog,
    GeoRuleType, GeoAction, DetectionMethod
)


class GeoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def configure_geo(self, tenant_id, enabled=True, default_action=GeoAction.BLOCK, vpn_detection_enabled=False, vpn_action=GeoAction.BLOCK, proxy_detection_enabled=False, proxy_action=GeoAction.BLOCK, bypass_prevention_enabled=True, redirect_url=None):
        existing = await self.db.execute(select(GeoConfiguration).where(GeoConfiguration.tenant_id == tenant_id))
        config = existing.scalar_one_or_none()
        if config:
            config.enabled = enabled
            config.default_action = default_action
            config.vpn_detection_enabled = vpn_detection_enabled
            config.vpn_action = vpn_action
            config.proxy_detection_enabled = proxy_detection_enabled
            config.proxy_action = proxy_action
            config.bypass_prevention_enabled = bypass_prevention_enabled
            config.redirect_url = redirect_url
            config.updated_at = datetime.utcnow()
        else:
            config = GeoConfiguration(tenant_id=tenant_id, enabled=enabled, default_action=default_action, vpn_detection_enabled=vpn_detection_enabled, vpn_action=vpn_action, proxy_detection_enabled=proxy_detection_enabled, proxy_action=proxy_action, bypass_prevention_enabled=bypass_prevention_enabled, redirect_url=redirect_url)
            self.db.add(config)
        await self.db.commit()
        await self.db.refresh(config)
        return config

    async def get_configuration(self, tenant_id):
        result = await self.db.execute(select(GeoConfiguration).where(GeoConfiguration.tenant_id == tenant_id))
        return result.scalar_one_or_none()

    async def create_rule(self, tenant_id, rule_type, action, country_code=None, region_code=None, content_id=None, content_type="all", priority=0, expires_at=None):
        rule = GeoRule(tenant_id=tenant_id, rule_type=rule_type, action=action, country_code=country_code, region_code=region_code, content_id=content_id, content_type=content_type, priority=priority, expires_at=expires_at)
        self.db.add(rule)
        await self.db.commit()
        await self.db.refresh(rule)
        return rule

    async def list_rules(self, tenant_id, active_only=True):
        query = select(GeoRule).where(GeoRule.tenant_id == tenant_id)
        if active_only:
            query = query.where(GeoRule.is_active == True)
        result = await self.db.execute(query.order_by(GeoRule.priority.desc()))
        return result.scalars().all()

    def _lookup_geo(self, ip_address):
        hash_val = int(hashlib.md5(ip_address.encode()).hexdigest()[:8], 16)
        countries = ["US", "GB", "DE", "FR", "JP", "CN", "AU", "CA", "BR", "IN"]
        regions = ["CA", "NY", "TX", "FL", "WA", "OR", "NV", "AZ", "CO", "IL"]
        return countries[hash_val % len(countries)], regions[hash_val % len(regions)]

    async def check_access(self, tenant_id, ip_address, content_id=None, content_type="all", user_agent=None, user_id=None):
        config = await self.get_configuration(tenant_id)
        if not config or not config.enabled:
            return True, GeoAction.ALLOW, None, None, False, False, None
        country_code, region_code = self._lookup_geo(ip_address)
        vpn_info = await self.detect_vpn(tenant_id, ip_address)
        is_vpn = vpn_info.is_vpn if vpn_info else False
        is_proxy = vpn_info.is_proxy if vpn_info else False
        if is_vpn and config.vpn_detection_enabled and config.vpn_action == GeoAction.BLOCK:
            return False, GeoAction.BLOCK, country_code, region_code, is_vpn, is_proxy, "VPN detected"
        if is_proxy and config.proxy_detection_enabled and config.proxy_action == GeoAction.BLOCK:
            return False, GeoAction.BLOCK, country_code, region_code, is_vpn, is_proxy, "Proxy detected"
        rules = await self.list_rules(tenant_id)
        for rule in rules:
            if rule.content_id and rule.content_id != content_id: continue
            if rule.content_type != "all" and rule.content_type != content_type: continue
            if rule.country_code and rule.country_code != country_code: continue
            if rule.region_code and rule.region_code != region_code: continue
            if rule.rule_type == GeoRuleType.BLOCK: return False, GeoAction.BLOCK, country_code, region_code, is_vpn, is_proxy, "Geo-blocked"
            else: return True, GeoAction.ALLOW, country_code, region_code, is_vpn, is_proxy, None
        action = config.default_action
        return action == GeoAction.ALLOW, action, country_code, region_code, is_vpn, is_proxy, None

    async def detect_vpn(self, tenant_id, ip_address):
        result = await self.db.execute(select(VPNDetection).where(VPNDetection.tenant_id == tenant_id, VPNDetection.ip_address == ip_address, VPNDetection.expires_at > datetime.utcnow()))
        existing = result.scalar_one_or_none()
        if existing: return existing
        hash_val = int(hashlib.md5(ip_address.encode()).hexdigest()[:2], 16)
        is_vpn, is_proxy, is_tor = hash_val < 10, hash_val >= 10 and hash_val < 20, hash_val >= 20 and hash_val < 25
        detection = VPNDetection(tenant_id=tenant_id, ip_address=ip_address, is_vpn=is_vpn, is_proxy=is_proxy, is_tor=is_tor, detection_method=DetectionMethod.IP_LOOKUP, confidence_score=0.9 if (is_vpn or is_proxy or is_tor) else 0.1, provider_name="VPNProvider" if is_vpn else None, expires_at=datetime.utcnow() + timedelta(hours=24))
        self.db.add(detection)
        await self.db.commit()
        await self.db.refresh(detection)
        return detection

    async def add_whitelist(self, tenant_id, country_code, region_code=None, content_id=None, content_type="all", notes=None):
        entry = GeoWhitelist(tenant_id=tenant_id, country_code=country_code, region_code=region_code, content_id=content_id, content_type=content_type, notes=notes)
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def add_blacklist(self, tenant_id, country_code, region_code=None, content_id=None, content_type="all", reason=None):
        entry = GeoBlacklist(tenant_id=tenant_id, country_code=country_code, region_code=region_code, content_id=content_id, content_type=content_type, reason=reason)
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry
