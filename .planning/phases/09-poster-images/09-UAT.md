# Phase 9 UAT: Poster Images

**Date:** 2026-04-29
**Tester:** AI Agent
**Status:** ⚠️ IN PROGRESS

## Previous Blocker - RESOLVED

### API Proxy Configuration - FIXED
The vite.config.ts now has the correct path rewrite for the API proxy.

**Fixed configuration:**
```typescript
proxy: {
  '/api/v1': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api\/v1/, ''),
  }
}
```

✅ Verified: API calls now reach backend (returns 401 Unauthorized instead of 404)

## Current Issue

### Database Schema Mismatch
The User model has `display_name` field but the database table lacks this column.

**Error:** `sqlite3.OperationalError: no such column: users.display_name`

**Impact:** Cannot create test users for login testing.

## Build Verification
- [x] TypeScript compilation passed
- [x] Vite build succeeded
- [x] API proxy configuration fixed

## Test Cases (Pending Database Fix)

### MED-01: Upload Poster
- [ ] Admin can upload image file
- [ ] Supported formats: JPEG, PNG, WebP, GIF
- [ ] Invalid formats rejected

### MED-02: Display Poster
- [ ] Poster shown in catalog cards
- [ ] Placeholder shown when no poster
- [ ] Image properly sized

## Result: ⚠️ IN PROGRESS - Database schema needs migration
