# Stack Research: CC Video

## Recommended Stack

### Frontend

- React + Vite for the web client.
- React Router for authenticated user/admin route separation.
- A standard HTML5 `<video>` player for v1 playback.
- Axios or Fetch for API calls.

Rationale: The app needs a catalog UI, login flows, admin forms, upload progress, and a browser video player. React/Vite is a low-friction fit for a separated frontend and can evolve without forcing a backend framework choice.

### Backend

- Node.js + Express for REST APIs.
- JWT or server-session based authentication with role checks.
- Multer or equivalent multipart middleware for local video uploads.
- Static/ranged file serving for uploaded video playback.

Rationale: Express is sufficient for v1 CRUD, auth, upload, and playback endpoints. The most important backend detail is not framework novelty; it is correct handling of upload validation, storage paths, permissions, and byte-range playback.

### Database

- PostgreSQL for users, roles, movies, metadata, and uploaded file records.
- Prisma or another migration-backed ORM if the implementation uses TypeScript.

Rationale: The data model is relational: users, admin roles, movies, files, and audit/status fields. PostgreSQL keeps this simple and production-friendly.

### File Storage

- Local filesystem storage for v1, with paths recorded in the database.
- Store uploaded files outside frontend build assets.
- Use a private upload directory and serve through backend-controlled endpoints.

Rationale: The user explicitly chose administrator-uploaded local video files. Keeping storage behind backend authorization prevents accidentally exposing files through public static hosting.

## What Not To Use For v1

- Do not start with distributed object storage unless deployment requires it.
- Do not build transcoding pipelines before basic upload/playback works.
- Do not introduce payments, recommendations, or real-time features into the first roadmap.

## Confidence

High for the architecture and feature split. Medium for specific libraries, because final implementation should follow the package ecosystem chosen during phase planning.
