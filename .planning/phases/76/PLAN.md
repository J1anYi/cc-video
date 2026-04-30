# Plan: Phase 76 - Multi-Tenant Architecture

## Goal
Implement tenant isolation and data segregation for multi-tenant platform support.

## Requirements

| ID | Requirement | Priority | Complexity |
|----|-------------|----------|------------|
| TENANT-01 | System supports multiple isolated tenants with separate data | Critical | High |
| TENANT-02 | Tenant data is completely isolated from other tenants | Critical | High |
| TENANT-03 | Users belong to specific tenants with tenant-scoped access | Critical | Medium |
| TENANT-04 | Tenant context automatically applied to all queries | Critical | Medium |
| TENANT-05 | Cross-tenant data access prevented at database level | Critical | High |

## Implementation Strategy

### Approach: Shared Database with Row-Level Tenant Isolation

**Rationale:**
- Lower operational overhead vs separate databases/schemas
- Easier to implement and maintain
- Suitable for v2.9 scope
- Can migrate to separate schemas in future if needed

## Tasks

### 1. Create Tenant Model
**File:** backend/app/models/tenant.py

Create Tenant model with:
- id, name, slug, plan, status, settings
- created_at, updated_at timestamps

### 2. Add Tenant Context to User Model
**File:** backend/app/models/user.py

Add tenant_id foreign key to User model.

### 3. Add Tenant Context to All Tenant-Scoped Models
**Files:** All model files for tenant-scoped entities

Add tenant_id to: Movie, VideoFile, Subtitle, VideoChapter, WatchHistory, Favorite, Watchlist, Review, Rating, Comment, Notification, Report, UserAnalytics, ViewingSession, TranscodingJob, AudioTrack, VideoQuality, UserBookmark.

### 4. Create Tenant Service
**File:** backend/app/services/tenant_service.py

Implement tenant resolution and management.

### 5. Create Tenant Middleware
**File:** backend/app/middleware/tenant.py

Middleware to extract tenant context from subdomain/header/user.

### 6. Create Tenant-Aware Query Scoping
**File:** backend/app/utils/tenant_scoping.py

Utility functions for automatic tenant filtering.

### 7. Update Dependencies
**File:** backend/app/dependencies.py

Add tenant-aware dependencies.

### 8. Update Auth Service
**File:** backend/app/services/auth.py

Add tenant_id to JWT claims.

### 9. Create Database Migration
**File:** backend/migrations/versions/add_tenant_support.py

Create Alembic migration for tenant tables.

### 10. Update All Routes with Tenant Scoping
**Files:** All route files

Update routes to use tenant-scoped queries.

### 11. Create Tenant Admin Routes
**File:** backend/app/routes/tenant_admin.py

Platform admin routes for tenant management.

### 12. Frontend: Tenant Context Provider
**File:** frontend/src/contexts/TenantContext.tsx

React context for tenant information.

### 13. Frontend: Update Auth Flow
**File:** frontend/src/auth/AuthContext.tsx

Update authentication to handle tenant.

### 14. Update Frontend API Client
**File:** frontend/src/api/client.ts

Add tenant context to API requests.

### 15. Create Alembic Migration
**File:** backend/migrations/versions/xxxx_add_tenant_support.py

Create and run migration script.

## File Changes Summary

### New Files
- backend/app/models/tenant.py
- backend/app/services/tenant_service.py
- backend/app/middleware/tenant.py
- backend/app/utils/tenant_scoping.py
- backend/app/routes/tenant_admin.py
- frontend/src/contexts/TenantContext.tsx

### Modified Files
- backend/app/models/user.py - Add tenant_id
- backend/app/models/movie.py - Add tenant_id
- backend/app/models/*.py - Add tenant_id to all scoped models
- backend/app/dependencies.py - Add tenant dependencies
- backend/app/services/auth.py - Add tenant to JWT
- backend/app/routes/*.py - Add tenant scoping
- frontend/src/auth/AuthContext.tsx - Handle tenant
- frontend/src/api/*.ts - Add tenant headers

## Security Considerations

1. Tenant ID Validation on every request
2. Query Scoping - All queries filtered by tenant
3. File Storage - Tenant-scoped directories
4. JWT Claims - Include tenant_id in token

## Success Criteria Verification

1. Multiple isolated tenants supported - Tenant model and migration
2. Tenant data completely isolated - Query scoping and middleware
3. Users belong to specific tenants - User.tenant_id relationship
4. Tenant context auto-applied - Middleware and dependencies
5. Cross-tenant access prevented - Security validation at all layers

---
*Created: 2026-04-30*
