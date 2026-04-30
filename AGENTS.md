<!-- GSD:project-start source:PROJECT.md -->
## Project

**CC Video**

CC Video is a web-based movie watching system with separated frontend and backend services. Regular users log in, browse a movie catalog, and play uploaded videos in the browser; administrators manage the movie library by uploading local video files and maintaining movie metadata.

The v1 product focuses on making the basic viewing loop work end to end: a user can log in, find a movie in the list, and watch it, while an administrator can add and manage the movies that appear there.

**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

### Constraints

- **Architecture**: Frontend and backend must be separated - this is an explicit project requirement.
- **Video source**: v1 movie content comes from administrator-uploaded local video files - external video URLs are out of scope.
- **Authentication**: Regular user login is required for viewing - anonymous viewing is not the initial model.
- **Web-first**: The viewing experience is delivered through a browser - native apps are deferred.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Recommended Stack
### Frontend
- React + Vite for the web client.
- React Router for authenticated user/admin route separation.
- A standard HTML5 `<video>` player for v1 playback.
- Axios or Fetch for API calls.
### Backend
- Node.js + Express for REST APIs.
- JWT or server-session based authentication with role checks.
- Multer or equivalent multipart middleware for local video uploads.
- Static/ranged file serving for uploaded video playback.
### Database
- PostgreSQL for users, roles, movies, metadata, and uploaded file records.
- Prisma or another migration-backed ORM if the implementation uses TypeScript.
### File Storage
- Local filesystem storage for v1, with paths recorded in the database.
- Store uploaded files outside frontend build assets.
- Use a private upload directory and serve through backend-controlled endpoints.
## What Not To Use For v1
- Do not start with distributed object storage unless deployment requires it.
- Do not build transcoding pipelines before basic upload/playback works.
- Do not introduce payments, recommendations, or real-time features into the first roadmap.
## Confidence
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
