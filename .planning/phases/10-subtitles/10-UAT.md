# Phase 10 UAT: Subtitles

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

### TC-1: Admin Upload Subtitle (MED-03)
- [ ] Login as admin
- [ ] Upload VTT/SRT file to movie via POST /admin/movies/{id}/subtitles
- [ ] Verify 200 OK, subtitle record created

### TC-2: User Get Subtitles (MED-04)
- [ ] Login as user
- [ ] GET /movies/{id}/subtitles
- [ ] Verify 200 OK, subtitle list returned

### TC-3: Multiple Subtitles (MED-05)
- [ ] Upload multiple subtitle files with different languages
- [ ] Verify all are stored separately

### TC-4: Frontend Subtitle Selection (MED-04)
- [ ] Open playback page
- [ ] Verify subtitle dropdown appears when subtitles exist
- [ ] Select different subtitle tracks

### TC-5: Delete Subtitle
- [ ] DELETE /admin/movies/{id}/subtitles/{subtitle_id}

## Result: ⚠️ IN PROGRESS - Database schema needs migration
