# Plan: Phase 121 - Digital Rights Management

## Goal
Implement comprehensive DRM support with multi-DRM provider integration, device registration, and offline playback capabilities.

## Tasks

### 1. Database Models
- [ ] Create DRMProvider enum (WIDEVINE, PLAYREADY, FAIRPLAY)
- [ ] Create DRMKeyStatus enum (ACTIVE, EXPIRED, REVOKED)
- [ ] Create DeviceType enum (WEB, IOS, ANDROID, SMART_TV, UNKNOWN)
- [ ] Create DRMConfiguration model
- [ ] Create DRMKey model
- [ ] Create DeviceRegistration model
- [ ] Create DRMLicense model
- [ ] Create OfflineDRMToken model

### 2. Service Layer
- [ ] Create DRMService with methods:
  - configure_drm()
  - generate_content_key()
  - issue_license()
  - register_device()
  - list_devices()
  - remove_device()
  - generate_offline_token()
  - rotate_keys()

### 3. API Routes
- [ ] POST /drm/config - Configure DRM
- [ ] GET /drm/config - Get configuration
- [ ] POST /drm/keys - Generate keys
- [ ] POST /drm/license - Issue license
- [ ] GET /drm/devices - List devices
- [ ] DELETE /drm/devices/{id} - Remove device
- [ ] POST /drm/offline-token - Offline token

### 4. Schemas
- [ ] DRMConfigCreate/Response
- [ ] DRMKeyCreate/Response
- [ ] LicenseRequest/Response
- [ ] DeviceRegistrationResponse
- [ ] OfflineTokenResponse

### 5. Frontend API
- [ ] drm.ts with TypeScript interfaces
- [ ] API client functions

### 6. Integration
- [ ] Register router in main.py
- [ ] Update ROADMAP/REQUIREMENTS/STATE

## Success Criteria
- All 5 DRM requirements implemented
- Device registration and limits working
- License issuance functional
- Offline token generation working
