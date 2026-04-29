# Roadmap: CC Video

**Created:** 2026-04-29
**Granularity:** Coarse
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Overview

| Phase | Name | Goal | Requirements | UI hint |
|-------|------|------|--------------|---------|
| 1 | Backend Foundation | Establish API, persistence, auth, roles, and project structure for separated frontend/backend development | AUTH-01, AUTH-02, AUTH-03, AUTH-04, API-01, API-02 | yes |
| 2 | Admin Movie Management | Allow administrators to create movie records, upload local video files, and control catalog visibility | ADM-01, ADM-02, ADM-03, ADM-04, ADM-05 | yes |
| 3 | User Catalog And Playback | Let logged-in users browse published movies and play uploaded videos securely in the browser | CAT-01, CAT-02, CAT-03, PLAY-01, PLAY-02, PLAY-03 | yes |
| 4 | Frontend Integration And Verification | Complete user/admin routes, connect all APIs, and verify the end-to-end viewing loop | API-03 | yes |

## Phase Details

### Phase 1: Backend Foundation

**Goal:** Establish the separated backend API foundation with database persistence, authentication, session behavior, and administrator role enforcement.

**Requirements:** AUTH-01, AUTH-02, AUTH-03, AUTH-04, API-01, API-02

**Success Criteria:**

1. Backend exposes documented auth and current-user APIs for the frontend.
2. Users, roles, movies, and uploaded video file metadata can be persisted in the database schema.
3. A regular user can log in, remain logged in across refresh, and log out.
4. Admin-only API requests are rejected for non-admin users.

**Notes:**

- This phase should choose the concrete backend framework, database library, and auth mechanism.
- Keep route contracts clear because the frontend is intentionally separate.

### Phase 2: Admin Movie Management

**Goal:** Build administrator workflows for creating movie records, uploading local video files, editing metadata, and controlling whether movies appear to users.

**Requirements:** ADM-01, ADM-02, ADM-03, ADM-04, ADM-05

**Success Criteria:**

1. Admin can create a movie with title, description, and publication status.
2. Admin can upload a local video file and attach it to a movie.
3. Admin can edit movie metadata and publish/unpublish or disable movies.
4. Removed or disabled movies no longer appear in the user catalog.
5. Upload validation prevents unsupported or missing video files from being published.

**Notes:**

- Store video files in a backend-controlled upload directory, not as public frontend assets.
- Track upload metadata in the database so playback can be authorized later.

### Phase 3: User Catalog And Playback

**Goal:** Build the logged-in viewer experience for browsing published movies and playing uploaded videos securely in the browser.

**Requirements:** CAT-01, CAT-02, CAT-03, PLAY-01, PLAY-02, PLAY-03

**Success Criteria:**

1. Logged-in users can view a list of published movies.
2. Movie catalog entries show title, description, and basic metadata.
3. User can open a movie playback page from the catalog.
4. Browser video playback works for an uploaded movie file.
5. Playback endpoints reject unauthenticated users.
6. Seeking works when the uploaded file format supports browser range playback.

**Notes:**

- Validate the complete media path with a small sample video before expanding UI polish.
- This phase should verify secure playback, not just render a video element.

### Phase 4: Frontend Integration And Verification

**Goal:** Complete the separated frontend routes for user and admin flows, connect them to backend APIs, and verify the full v1 product loop end to end.

**Requirements:** API-03

**Success Criteria:**

1. Frontend has separate logged-in user routes and admin-only management routes.
2. API client handles auth state consistently across user and admin pages.
3. A complete admin-to-user flow works: admin uploads and publishes a movie, user logs in, user finds it in the catalog, user plays it.
4. End-to-end verification covers login, admin upload, catalog display, authorized playback, and logout.
5. README or project guide explains how to run frontend and backend locally.

**Notes:**

- This phase is intentionally integration-heavy because earlier phases may build backend and frontend slices separately.
- Any missing route, API, or state handling required for v1 should be closed here.

## Coverage Validation

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 1 | Pending |
| AUTH-02 | Phase 1 | Pending |
| AUTH-03 | Phase 1 | Pending |
| AUTH-04 | Phase 1 | Pending |
| CAT-01 | Phase 3 | Pending |
| CAT-02 | Phase 3 | Pending |
| CAT-03 | Phase 3 | Pending |
| PLAY-01 | Phase 3 | Pending |
| PLAY-02 | Phase 3 | Pending |
| PLAY-03 | Phase 3 | Pending |
| ADM-01 | Phase 2 | Pending |
| ADM-02 | Phase 2 | Pending |
| ADM-03 | Phase 2 | Pending |
| ADM-04 | Phase 2 | Pending |
| ADM-05 | Phase 2 | Pending |
| API-01 | Phase 1 | Pending |
| API-02 | Phase 1 | Pending |
| API-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Roadmap created: 2026-04-29*
