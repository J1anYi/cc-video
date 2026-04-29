# Phase 2: Admin Movie Management - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase builds administrator workflows for creating movie records, uploading local video files, editing metadata, and controlling whether movies appear to users. The frontend admin UI is intentionally separate — this phase delivers backend APIs and database operations for movie management.

**In scope:**
- Backend API endpoints for movie CRUD operations
- Video file upload handling and storage
- Movie metadata management (title, description, publication status)
- Publication status control (draft, published, disabled)
- Video file attachment to movie records
- Database operations for movie and video file entities

**Out of scope:**
- Frontend admin UI implementation (Phase 4)
- User-facing catalog display (Phase 3)
- Video playback serving (Phase 3)
- Video transcoding or optimization

</domain>

<decisions>
## Implementation Decisions

### Video Upload Handling
- **D-01:** Use **multipart/form-data file upload** via FastAPI's `UploadFile`
  - Rationale: Standard approach for file uploads in FastAPI, handles streaming for large files, automatic content-type validation. Works well with the existing async architecture from Phase 1.
  - [auto] Selected as recommended standard approach.

### Video Storage
- **D-02:** Store video files in a **backend-controlled upload directory** with database metadata tracking
  - Rationale: Files stored under `backend/uploads/videos/` with unique generated filenames to prevent collisions. Database tracks file_path, file_size, mime_type, and movie association. This separates uploaded content from codebase and enables access control.
  - [auto] Selected as recommended for v1 simplicity.

### Movie Update Behavior
- **D-03:** Support **partial updates** with optional video file replacement
  - Rationale: PATCH-style updates where title, description, and publication_status can be updated independently. Video files can be added, replaced, or removed separately. This matches typical admin workflow where metadata and media are managed separately.
  - [auto] Selected as recommended for admin flexibility.

### Delete vs Disable Behavior
- **D-04:** Implement **soft delete via DISABLED status** for movies
  - Rationale: Movies with DISABLED status are hidden from user catalog but retained in database for audit/recovery. Hard delete available as separate admin action with confirmation. PublicationStatus enum already supports this pattern.
  - [auto] Selected as recommended for data safety.

### API Structure
- **D-05:** Use **RESTful admin endpoints** under `/admin/movies/`
  - Rationale: Consistent with existing admin router pattern from Phase 1. Endpoints: GET /movies (list all), POST /movies (create), GET /movies/{id} (detail), PATCH /movies/{id} (update), DELETE /movies/{id} (hard delete), POST /movies/{id}/video (upload video), DELETE /movies/{id}/video (remove video).
  - [auto] Selected as recommended REST pattern.

### Video Validation
- **D-06:** Validate **file type and size** on upload
  - Rationale: Accept only video MIME types (video/mp4, video/webm, etc.). Maximum file size configurable via settings (default 500MB for v1). Return clear error messages for invalid uploads.
  - [auto] Selected as recommended for security and UX.

### Claude's Discretion
- Exact file naming convention for uploaded videos
- Error response format details
- Logging configuration for upload operations
- Progress reporting during upload (if needed)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Documentation
- `.planning/PROJECT.md` — Project vision, constraints, key decisions
- `.planning/REQUIREMENTS.md` — ADM-01, ADM-02, ADM-03, ADM-04, ADM-05 requirements
- `.planning/ROADMAP.md` — Phase 2 goal and success criteria

### Prior Phase Context
- `.planning/phases/01-backend-foundation/01-CONTEXT.md` — Phase 1 decisions (FastAPI, SQLAlchemy, RBAC middleware)

### External References (to be consulted)
- FastAPI file upload documentation — https://fastapi.tiangolo.com/tutorial/request-files/
- FastAPI background tasks for post-upload processing — https://fastapi.tiangolo.com/tutorial/background-tasks/

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/app/models/movie.py` — Movie and PublicationStatus already defined
- `backend/app/models/video_file.py` — VideoFile model exists with movie relationship
- `backend/app/routes/admin.py` — Admin router with placeholder endpoints ready to extend
- `backend/app/schemas/movie.py` — MovieCreate, MovieResponse schemas exist
- `backend/app/middleware/rbac.py` — RBAC middleware for admin role enforcement
- `backend/app/config.py` — Settings class ready for upload config additions

### Established Patterns
- Async SQLAlchemy 2.0 with `Mapped[]` type hints
- Pydantic v2 schemas with `from_attributes = True`
- FastAPI dependencies for auth and RBAC
- Router-level admin enforcement via `dependencies=[admin_required]`

### Integration Points
- Admin router at `/admin/movies/` — extend existing placeholder endpoints
- Video files stored in `backend/uploads/videos/` (new directory)
- Database already has movies and video_files tables

</code_context>

<specifics>
## Specific Ideas

- Video upload should feel fast even for large files — streaming upload is important
- Admin should see clear error messages if upload fails validation
- Consider adding file size to settings for easy configuration
- Movie creation and video upload are separate operations — create movie first, then upload video

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-admin-movie-management*
*Context gathered: 2026-04-29*
