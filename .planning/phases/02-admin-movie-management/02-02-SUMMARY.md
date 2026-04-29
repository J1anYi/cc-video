# Plan 02-02: Video Upload Service and Admin Route Implementations

**Status:** Completed
**Started:** 2026-04-29T06:12:17Z
**Completed:** 2026-04-29T06:XX:XXZ

## Summary

Implemented video file upload service and connected admin routes to movie/video services, enabling administrators to upload video files and manage movie records through RESTful API endpoints.

## Tasks Completed

### Task 1: Create VideoFileResponse schema
- Created `backend/app/schemas/video_file.py`
- Defined `VideoFileResponse` with id, movie_id, filename, file_size, mime_type, created_at
- Intentionally excluded `file_path` for security (internal storage detail)
- Updated `backend/app/schemas/__init__.py` to export `VideoFileResponse`
- Added `from __future__ import annotations` to `movie.py` for forward reference resolution

### Task 2: Create video file service
- Created `backend/app/services/video_file.py`
- Implemented `VideoFileService` with:
  - `upload(db, movie_id, file)`: Validates MIME type, file size, saves to disk with UUID filename
  - `get_by_movie(db, movie_id)`: Returns all video files for a movie
  - `get_by_id(db, video_file_id)`: Returns single video file
  - `delete(db, video_file_id)`: Removes file from disk and database
- Validates against `settings.ALLOWED_VIDEO_TYPES` and `settings.MAX_VIDEO_SIZE`
- Uses UUID-prefixed filenames to prevent collisions

### Task 3: Update admin routes
- Rewrote `backend/app/routes/admin.py` with real implementations
- Endpoints implemented:
  - `POST /admin/movies` - Create movie
  - `GET /admin/movies` - List all movies (admin view)
  - `GET /admin/movies/{id}` - Get single movie
  - `PATCH /admin/movies/{id}` - Update movie
  - `DELETE /admin/movies/{id}` - Delete movie
  - `POST /admin/movies/{id}/video` - Upload video file
  - `DELETE /admin/movies/{id}/video` - Remove video file
- All endpoints use `movie_service` and `video_file_service`
- All endpoints require admin role via RBAC middleware

### Task 4: Create uploads directory
- Created `backend/uploads/videos/` directory
- Added `.gitkeep` file for version control tracking

### Task 5: Write integration tests
- Created `tests/test_admin_routes.py`
- 17 test cases covering:
  - Movie CRUD operations
  - Video upload validation
  - RBAC enforcement
  - Error handling (404, 400, 403, 401)

## Files Modified

- `backend/app/schemas/video_file.py` (created)
- `backend/app/schemas/movie.py` (updated - added future annotations)
- `backend/app/schemas/__init__.py` (updated - added VideoFileResponse export)
- `backend/app/services/video_file.py` (created)
- `backend/app/routes/admin.py` (rewritten)
- `backend/uploads/videos/.gitkeep` (created)
- `tests/test_admin_routes.py` (created)

## Verification

All requirements verified:
- [x] Admin can upload a video file and attach it to a movie record
- [x] Admin can remove a video file from a movie
- [x] Video files are stored in backend/uploads/videos/ with unique filenames
- [x] Video file metadata is tracked in database
- [x] Upload validation rejects non-video MIME types and oversized files
- [x] Admin routes are accessible at /admin/movies/ endpoints
- [x] All admin endpoints require admin role via RBAC middleware

## Commits

All changes auto-committed via agent checkpoint system.

## Next Steps

Plan 02-03 should implement user-facing movie catalog and video playback endpoints.
