# Pitfalls Research: CC Video

## Pitfall: Treating Videos Like Small Images

Large videos need upload limits, progress UI, storage planning, and playback streaming. Prevent this by designing file metadata, upload validation, and playback endpoints before building the admin UI.

## Pitfall: Publishing Broken Uploads

If a movie appears in the catalog before its file is usable, users hit dead playback pages. Prevent this with movie status fields such as draft, published, and disabled.

## Pitfall: Public Static Video Exposure

Serving uploaded files directly from a public folder can bypass login. Prevent this by storing files in a backend-controlled location and serving through authenticated endpoints.

## Pitfall: Role Checks Only In The Frontend

Admin pages hidden in the UI are not real security. Prevent this with backend role checks on every admin API and upload endpoint.

## Pitfall: Leaving Playback Untested Until Late

The hardest part is the end-to-end path from uploaded file to browser playback. Prevent this by making a small uploaded sample video playable early in the roadmap.

## Phase Mapping

- Phase 1 should establish auth, roles, and core data model.
- Phase 2 should prove admin upload and movie management.
- Phase 3 should prove user catalog and playback.
- Phase 4 should integrate frontend flows and verify end-to-end behavior.
