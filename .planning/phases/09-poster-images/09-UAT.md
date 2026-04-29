# Phase 9 UAT: Poster Images

**Date:** 2026-04-29
**Tester:** AI Agent
**Status:** ❌ BLOCKED

## Critical Blocker

### API Proxy Configuration Missing
The vite.config.ts is missing the required path rewrite for the API proxy. This causes all API calls to fail with 404.

**Current (broken) configuration:**
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

**Required fix:**
```typescript
proxy: {
  '/api/v1': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api\/v1/, ''),
  }
}
```

## Browser Test Results

### Login Test
- [x] Navigate to http://127.0.0.1:5181
- [x] Page loads correctly (redirects to /login)
- [x] Fill email: test@example.com
- [x] Fill password: testpassword123
- [x] Click Login button
- [ ] ❌ API call fails: `404 (Not Found) @ http://127.0.0.1:5181/api/v1/auth/login`

## Root Cause
Frontend requests `/api/v1/auth/login` → vite proxy forwards to `http://localhost:8000/api/v1/auth/login` → 404 (backend route is `/auth/login`)

## Required Action
Fix `frontend/vite.config.ts` to add path rewrite that strips `/api/v1` prefix before forwarding to backend.

## Test Cases (Pending Fix)

### MED-01: Upload Poster
- [ ] Admin can upload image file (BLOCKED - cannot login)
- [ ] Supported formats: JPEG, PNG, WebP, GIF
- [ ] Invalid formats rejected

### MED-02: Display Poster
- [ ] Poster shown in catalog cards (BLOCKED - cannot access catalog)
- [ ] Placeholder shown when no poster
- [ ] Image properly sized

## Build Verification
- [x] TypeScript compilation passed
- [x] Vite build succeeded

## Result: ❌ BLOCKED - API proxy misconfiguration
