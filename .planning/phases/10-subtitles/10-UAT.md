# Phase 10 UAT: Subtitles

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

### TC-1: Admin Upload Subtitle (MED-03)
- [ ] Login as admin (BLOCKED)
- [ ] Upload VTT/SRT file to movie via POST /admin/movies/{id}/subtitles
- [ ] Verify 200 OK, subtitle record created

### TC-2: User Get Subtitles (MED-04)
- [ ] Login as user (BLOCKED)
- [ ] GET /movies/{id}/subtitles
- [ ] Verify 200 OK, subtitle list returned

### TC-3: Multiple Subtitles (MED-05)
- [ ] Upload multiple subtitle files with different languages (BLOCKED)
- [ ] Verify all are stored separately

### TC-4: Frontend Subtitle Selection (MED-04)
- [ ] Open playback page (BLOCKED - cannot login)
- [ ] Verify subtitle dropdown appears when subtitles exist
- [ ] Select different subtitle tracks

### TC-5: Delete Subtitle
- [ ] DELETE /admin/movies/{id}/subtitles/{subtitle_id} (BLOCKED - cannot login)

## Build Verification
- [x] TypeScript compilation passed
- [x] Vite build succeeded

## Result: ❌ BLOCKED - API proxy misconfiguration
