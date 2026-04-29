# Phase 11 UAT: Password Reset

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

### TC-01: Navigate to Forgot Password
- [x] Navigate to http://127.0.0.1:5181/login
- [x] Click "Forgot password?" link
- [x] Page navigates to /forgot-password ✅

### TC-02: Request Password Reset
- [x] Fill email: test@example.com
- [x] Click "Send Reset Link"
- [ ] ❌ API call fails: `404 (Not Found) @ http://127.0.0.1:5181/api/v1/auth/password-reset`

## Root Cause
Frontend requests `/api/v1/auth/password-reset` → vite proxy forwards to `http://localhost:8000/api/v1/auth/password-reset` → 404 (backend route is `/auth/password-reset`)

## Required Action
Fix `frontend/vite.config.ts` to add path rewrite that strips `/api/v1` prefix before forwarding to backend.

## Test Cases (Pending Fix)

### TC-01: Request Password Reset (Existing Email)
- [ ] Enter existing email (BLOCKED - API 404)
- [ ] Verify success message
- [ ] Verify reset token created

### TC-02: Request Password Reset (Non-existing Email)
- [ ] Enter non-existing email (BLOCKED - API 404)
- [ ] Verify success message (no enumeration)

### TC-03: Reset Password with Valid Token
- [ ] Navigate to /reset-password?token=VALID_TOKEN (BLOCKED)
- [ ] Enter new password
- [ ] Verify password updated

### TC-04: Reset Password with Expired Token
- [ ] Test with expired token (BLOCKED)

### TC-05: Reset Password with Used Token
- [ ] Test with used token (BLOCKED)

### TC-06: Password Validation
- [ ] Test short password (BLOCKED)

### TC-07: Password Mismatch
- [ ] Test mismatched passwords (BLOCKED)

### TC-08: Login After Password Reset
- [ ] Login with new password (BLOCKED)

### TC-09: Missing Token in URL
- [ ] Navigate to /reset-password without token (BLOCKED)

## Build Verification
- [x] TypeScript compilation passed
- [x] Vite build succeeded

## Result: ❌ BLOCKED - API proxy misconfiguration
