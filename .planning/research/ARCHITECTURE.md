# Architecture Research: CC Video

## Components

### Frontend Web App

- User area: login, movie list, movie detail/playback page.
- Admin area: login-aware admin routes, movie list, create/edit form, video upload form.
- API client: shared request handling and auth token/session behavior.

### Backend API

- Auth module: login, session/token issuance, current user endpoint.
- User/role module: distinguish normal users from administrators.
- Movie module: CRUD metadata and catalog queries.
- Upload module: multipart upload, validation, storage, database file record.
- Playback module: authorized video response with byte-range support.

### Database

- users
- movies
- video_files or movie_assets
- sessions/tokens if session storage is used

### Local Storage

- Uploaded video files stored under a backend-owned upload directory.
- Database stores file path, original filename, MIME type, size, and movie association.

## Data Flow

1. Admin logs in and uploads a video with movie metadata.
2. Backend validates role, validates file type/size, stores the file, and writes movie/file records.
3. Regular user logs in and requests the movie catalog.
4. Backend returns published movies.
5. User opens playback page.
6. Frontend requests the playback URL through authenticated access.
7. Backend streams the file to the browser video player.

## Suggested Build Order

1. Backend foundation, database schema, auth, and role checks.
2. Admin movie CRUD and local video upload.
3. User catalog and playback API.
4. Frontend user/admin flows wired to APIs.
5. Verification, polish, and deployment hardening.

## Architectural Watchpoints

- Never expose upload directories directly without authorization.
- Keep admin and user permissions explicit.
- Validate uploads before storing or publishing.
- Support browser playback behavior early, not at the end.
