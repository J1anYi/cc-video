# Phase 124: Access Control

## Requirements

- AC-01: Content-level permissions
- AC-02: Time-based access windows
- AC-03: Device limit enforcement
- AC-04: Concurrent stream limits
- AC-05: Role-based content access

## Technical Approach

### Models
- AccessPolicy, ContentPermission, TimeWindow, DeviceLimit, StreamSession

### Enums
- AccessLevel: FULL, LIMITED, PREVIEW, NONE
- TimeWindowType: ALLOWED, RESTRICTED
- PermissionType: VIEW, DOWNLOAD, SHARE

### Service Layer
- AccessControlService: Permission evaluation, session management

### API Endpoints
- POST /access/policies, GET /access/policies
- POST /access/permissions, POST /access/check
- GET /access/sessions, DELETE /access/sessions/{id}
