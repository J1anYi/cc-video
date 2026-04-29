---
status: testing
phase: 05-movie-search-filtering
source:
  - 05-01-SUMMARY.md
  - 05-02-SUMMARY.md
  - 05-03-SUMMARY.md
started: 2026-04-29T10:05:00Z
updated: 2026-04-29T10:10:00Z
---

## Current Test

number: 1
name: API Path Configuration
expected: Frontend API requests should correctly proxy to backend endpoints
awaiting: fix required

## Tests

### 1. API Path Configuration
expected: Frontend API_BASE (/api/v1) should correctly proxy to backend endpoints via vite proxy
result: issue
reported: "Frontend requests /api/v1/auth/login but vite proxy forwards to http://localhost:8000/api/v1/auth/login which returns 404. Backend actual path is /auth/login. The vite proxy needs path rewrite: rewrite: (path) => path.replace(/^\/api\/v1/, '')"
severity: blocker
diagnosis: |
  - Frontend API_BASE = '/api/v1' in frontend/src/api/auth.ts
  - Vite proxy: '/api' -> 'http://localhost:8000' (no path rewrite)
  - Backend routes: /auth/login, /movies, /categories, etc.
  - Result: /api/v1/auth/login proxied to http://localhost:8000/api/v1/auth/login (404)
  - Expected: Should reach http://localhost:8000/auth/login

### 2. Search Movies by Title
expected: User can type in search box to filter movies by title (case-insensitive, partial match)
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

### 3. Filter by Category
expected: User can select a category from dropdown to filter movies
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

### 4. Combined Search and Category Filter
expected: Search and category filters work together
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

### 5. Clear Filters Button
expected: Clear Filters button appears when filters active and resets both filters
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

### 6. Empty Results State
expected: "No movies found" message displays when no results match
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

### 7. Category Badge Display
expected: Category badge visible on each movie card
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

### 8. Backend API Endpoints
expected: |
  - GET /movies - returns all published movies
  - GET /movies?q={term} - returns filtered movies
  - GET /movies?category={cat} - returns filtered movies
  - GET /categories - returns category list
result: pending
blocked_by: api-configuration
reason: Cannot test until API proxy is fixed

## Summary

total: 8
passed: 0
issues: 1
pending: 7
skipped: 0
blocked: 7

## Gaps

- truth: "Frontend API requests should successfully reach backend endpoints"
  status: failed
  reason: "API path mismatch: frontend uses /api/v1 prefix but vite proxy does not rewrite paths. Backend expects /auth/login, /movies, etc. without /api/v1 prefix."
  severity: blocker
  test: 1
  artifacts:
    - frontend/src/api/auth.ts (API_BASE = '/api/v1')
    - frontend/vite.config.ts (proxy without rewrite)
  missing:
    - Path rewrite configuration in vite proxy
  fix: |
    Update vite.config.ts to add path rewrite:
    ```typescript
    server: {
      proxy: {
        '/api/v1': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/v1/, ''),
        }
      }
    }
    ```
