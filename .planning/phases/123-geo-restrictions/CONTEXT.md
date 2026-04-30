# Phase 123: Geo-Restrictions

## Requirements

- GR-01: Country-based content blocking
- GR-02: Region-specific licensing
- GR-03: IP-based access control
- GR-04: VPN detection
- GR-05: Geo-bypass prevention

## Technical Approach

### Models
- GeoConfiguration: Geo-restriction settings per tenant
- GeoRule: Geographic access rules
- GeoWhitelist: Allowed regions
- GeoBlacklist: Blocked regions
- VPNDetection: VPN/proxy detection records
- GeoAccessLog: Access attempt logs

### Enums
- GeoRuleType: ALLOW, BLOCK
- GeoAction: ALLOW, BLOCK, REDIRECT
- DetectionMethod: IP_LOOKUP, VPN_DATABASE, BEHAVIORAL

### Service Layer
- GeoService: Rule evaluation, IP lookup, VPN detection

### API Endpoints
- POST /geo/config - Configure geo settings
- GET /geo/config - Get configuration
- POST /geo/rules - Create geo rule
- GET /geo/rules - List rules
- POST /geo/check - Check access for IP
- GET /geo/vpn-detect - VPN detection status
- GET /geo/logs - Access logs

## Integration Points
- Content filtering based on region
- Tenant-aware configuration
- IP geolocation integration
