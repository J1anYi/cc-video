# Phase 3: User Catalog And Playback - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase builds the logged-in user experience for browsing published movies and playing uploaded videos securely in the browser. The backend delivers catalog APIs and authenticated video streaming.

**In scope:**
- Backend API endpoints for movie catalog (published movies only)
- Authenticated video file serving with range request support
- Movie detail endpoint for playback page
- User-facing routes (separate from admin routes)
- Video streaming with seeking support

**Out of scope:**
- Frontend UI implementation (Phase 4)
- Admin movie management (Phase 2 - already complete)
- User authentication (Phase 1 - already complete)
- Video upload handling (Phase 2 - already complete)

</domain>

<decisions>
## Implementation Decisions

### Catalog API Structure
- **D-01:** Use **GET /movies** endpoint for published movie list
  - Rationale: RESTful convention, matches existing admin pattern. Returns only PUBLISHED movies. Uses existing movie_service.get_published() method.
  - [auto] Selected as recommended REST pattern.

### Movie Detail Endpoint
- **D-02:** Use **GET /movies/{id}** for single movie detail
  - Rationale: Standard REST pattern, needed for playback page to get movie info and video file reference.
  - [auto] Selected as recommended REST pattern.

### Video Playback Endpoint
- **D-03:** Use **GET /movies/{id}/stream** for authenticated video serving
  - Rationale: Separate endpoint allows auth check before serving files. Uses Range header for seeking support. Returns video file with proper Content-Type and Content-Range headers.
  - [auto] Selected as recommended for secure video streaming.

### Video Streaming Approach
- **D-04:** Implement **Range header support** for seeking
  - Rationale: Browser video players require Range requests for seeking. FastAPI's FileResponse supports this automatically. Return 206 Partial Content for range requests.
  - [auto] Selected as required for PLAY-03.

### Authentication Enforcement
- **D-05:** All user catalog endpoints require **authenticated user** (any role)
  - Rationale: Per requirements, only logged-in users can browse catalog and play videos. Uses existing get_current_user dependency from Phase 1.
  - [auto] Selected as per AUTH requirements.

### Response Format
- **D-06:** Use **MovieResponse schema** (already exists) for catalog responses
  - Rationale: Consistent with admin endpoints, includes all needed fields (id, title, description, publication_status, timestamps).
  - [auto] Selected for consistency with existing code.

### Claude's Discretion
- Exact error response format for unauthorized access
- Pagination default values
- Logging for video streaming operations

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Documentation
- `.planning/PROJECT.md` — Project vision, constraints, key decisions
- `.planning/REQUIREMENTS.md` — CAT-01, CAT-02, CAT-03, PLAY-01, PLAY-02, PLAY-03 requirements
- `.planning/ROADMAP.md` — Phase 3 goal and success criteria

### Prior Phase Context
- `.planning/phases/01-backend-foundation/01-CONTEXT.md` — Phase 1 decisions (FastAPI, JWT auth, RBAC)
- `.planning/phases/02-admin-movie-management/02-CONTEXT.md` — Phase 2 decisions (movie service, video upload)

### External References (to be consulted)
- FastAPI file response documentation — https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse
- HTTP Range requests — https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/app/services/movie.py` — movie_service with get_published(), get_by_id() methods
- `backend/app/services/video_file.py` — video_file_service with get_by_movie() method
- `backend/app/schemas/movie.py` — MovieResponse, MovieListResponse schemas
- `backend/app/dependencies.py` — get_current_user, get_db dependencies
- `backend/app/models/movie.py` — Movie model with PublicationStatus enum
- `backend/app/models/video_file.py` — VideoFile model with file_path, mime_type

### Established Patterns
- Async SQLAlchemy 2.0 with `Mapped[]` type hints
- Pydantic v2 schemas with `from_attributes = True`
- FastAPI dependencies for auth (get_current_user)
- Router-level auth enforcement via dependencies

### Integration Points
- User routes at `/movies/` — new router for user-facing endpoints
- Video files stored in `backend/uploads/videos/` (created in Phase 2)
- Database already has movies and video_files tables

</code_context>

<specifics>
## Specific Ideas

- Video streaming should feel instant — Range header support is essential
- Unauthorized users should see clear 401 error when accessing catalog
- Published movies only visible to logged-in users (not public)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 03-user-catalog-playback*
*Context gathered: 2026-04-29*
