# Phase 2: Admin Movie Management - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-29
**Phase:** 02-admin-movie-management
**Areas discussed:** Video Upload Handling, Video Storage, Movie Update Behavior, Delete vs Disable Behavior, API Structure, Video Validation

---

## Video Upload Handling

| Option | Description | Selected |
|--------|-------------|----------|
| Multipart/form-data with UploadFile | Standard FastAPI approach, streaming support, content-type validation | ✓ |
| Base64 encoded JSON payload | Simpler for small files, but inefficient for large videos | |
| Pre-signed URL upload | Cloud storage pattern, adds complexity | |

**User's choice:** Multipart/form-data with UploadFile (auto-selected - recommended)
**Notes:** Standard approach for file uploads in FastAPI, handles streaming for large files.

---

## Video Storage

| Option | Description | Selected |
|--------|-------------|----------|
| Backend upload directory + DB metadata | Files in controlled directory, database tracks metadata | ✓ |
| Database BLOB storage | Store files in database, simpler backup | |
| Cloud storage (S3, etc.) | Scalable but adds infrastructure complexity | |

**User's choice:** Backend upload directory + DB metadata (auto-selected - recommended)
**Notes:** Separates uploaded content from codebase, enables access control, simple for v1.

---

## Movie Update Behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Partial updates (PATCH-style) | Independent updates to title, description, status, video | ✓ |
| Full replacement updates | All fields required on each update | |
| Separate endpoints per field | Granular control but more endpoints | |

**User's choice:** Partial updates (auto-selected - recommended)
**Notes:** Matches typical admin workflow where metadata and media are managed separately.

---

## Delete vs Disable Behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Soft delete via DISABLED status | Hidden from catalog, retained in database | ✓ |
| Hard delete only | Permanently removes movie | |
| Both soft and hard delete options | Flexible but more complex UI | |

**User's choice:** Soft delete via DISABLED status (auto-selected - recommended)
**Notes:** PublicationStatus enum already supports this pattern. Hard delete available as separate action.

---

## API Structure

| Option | Description | Selected |
|--------|-------------|----------|
| RESTful endpoints under /admin/movies/ | Standard REST pattern, consistent with Phase 1 | ✓ |
| GraphQL mutations | Flexible queries, but adds complexity | |
| RPC-style endpoints | Action-based, less standard | |

**User's choice:** RESTful endpoints (auto-selected - recommended)
**Notes:** GET /movies, POST /movies, GET /movies/{id}, PATCH /movies/{id}, DELETE /movies/{id}, POST /movies/{id}/video, DELETE /movies/{id}/video.

---

## Video Validation

| Option | Description | Selected |
|--------|-------------|----------|
| File type + size validation | Security and UX, configurable limits | ✓ |
| File type only | Simpler, but no size protection | |
| No validation | Maximum flexibility, security risk | |

**User's choice:** File type + size validation (auto-selected - recommended)
**Notes:** Accept video MIME types only, max file size configurable via settings (default 500MB).

---

## Claude's Discretion

- Exact file naming convention for uploaded videos
- Error response format details
- Logging configuration for upload operations
- Progress reporting during upload (if needed)

## Deferred Ideas

None — discussion stayed within phase scope.
