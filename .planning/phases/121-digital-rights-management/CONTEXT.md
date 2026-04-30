# Phase 121: Digital Rights Management (DRM)

## Requirements

- DRM-01: Multi-DRM support (Widevine, PlayReady, FairPlay)
- DRM-02: License server integration
- DRM-03: Device registration and limits
- DRM-04: Offline playback with DRM
- DRM-05: Key rotation and management

## Technical Approach

### Models
- DRMConfiguration: DRM system settings per tenant
- DRMKey: Content encryption keys
- DeviceRegistration: User device tracking
- DRMLicense: License issuance records
- OfflineDRMToken: Offline playback tokens

### Enums
- DRMProvider: WIDEVINE, PLAYREADY, FAIRPLAY
- DRMKeyStatus: ACTIVE, EXPIRED, REVOKED
- DeviceType: WEB, IOS, ANDROID, SMART_TV, UNKNOWN

### Service Layer
- DRMService: Key generation, license issuance, device management

### API Endpoints
- POST /drm/config - Configure DRM settings
- GET /drm/config - Get current configuration
- POST /drm/keys - Generate content keys
- POST /drm/license - Issue playback license
- GET /drm/devices - List registered devices
- DELETE /drm/devices/{id} - Remove device
- POST /drm/offline-token - Generate offline token

## Integration Points
- Links to movies via content_id
- Tenant-aware configuration
- User device limits enforcement
