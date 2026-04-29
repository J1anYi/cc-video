# Research Summary: CC Video

## Stack

Use a separated React/Vite frontend and Node.js/Express backend, with PostgreSQL for relational data and backend-controlled local filesystem storage for uploaded videos. Keep the browser player simple in v1 with HTML5 video and backend playback endpoints.

## Table Stakes

- User login and session persistence.
- Admin role enforcement.
- Movie catalog for logged-in users.
- Admin movie CRUD.
- Local video upload.
- Browser playback of uploaded videos.
- Clear API boundary between frontend and backend.

## Watch Out For

- Local files must not be exposed as unauthenticated public assets.
- Playback should support browser video behavior, including range requests where needed.
- Uploaded movies should have publication status so incomplete uploads do not appear to users.
- Admin permissions must be enforced by backend APIs, not only frontend routing.

## Roadmap Implications

Build the backend foundation first, then admin upload management, then user catalog/playback, then frontend integration and verification. This order validates the riskiest media path before spending too much time on polish.
