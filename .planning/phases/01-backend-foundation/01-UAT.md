---
status: testing
phase: 01-backend-foundation
source:
  - 01-01-SUMMARY.md
  - 01-02-SUMMARY.md
  - 01-03-SUMMARY.md
  - 01-04-SUMMARY.md
  - 01-05-SUMMARY.md
started: 2026-04-29T15:00:00Z
updated: 2026-04-29T15:00:00Z
---

## Current Test

number: 1
name: Cold Start Smoke Test
expected: |
  Kill any running server/service. Clear ephemeral state (temp DBs, caches, lock files).
  Start the application from scratch. Server boots without errors, any seed/migration completes,
  and a primary query (health check, homepage load, or basic API call) returns live data.
awaiting: user response

## Tests

### 1. Cold Start Smoke Test
expected: Kill any running server/service. Clear ephemeral state. Start the application from scratch. Server boots without errors, and health check returns live data.
result: pending

### 2. Health Endpoint
expected: GET /health returns {"status": "healthy"} with 200 OK status
result: pending

### 3. OpenAPI Documentation
expected: GET /docs or GET /openapi.json returns valid API documentation
result: pending

### 4. User Registration
expected: POST /auth/login with valid credentials returns access_token and sets refresh_token cookie
result: pending

### 5. User Login
expected: Existing user can login with email/password and receive access token
result: pending

### 6. Session Persistence
expected: User can refresh access token using refresh_token cookie
result: pending

### 7. Current User Profile
expected: GET /auth/me with valid token returns user profile (id, email, role)
result: pending

### 8. User Logout
expected: POST /auth/logout clears refresh_token cookie
result: pending

### 9. Admin Access Control
expected: Non-admin user cannot access /admin/* endpoints (returns 403 Forbidden)
result: pending

### 10. Admin Dashboard Access
expected: Admin user can access /admin/dashboard endpoint
result: pending

### 11. Database Persistence
expected: User data, movies, and video files are persisted in SQLite database
result: pending

## Summary

total: 11
passed: 0
issues: 0
pending: 11
skipped: 0

## Gaps

[none yet]
