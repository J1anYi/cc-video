# CC Video

## What This Is

CC Video is a web-based movie watching system with separated frontend and backend services. Regular users log in, browse a movie catalog, and play uploaded videos in the browser; administrators manage the movie library by uploading local video files and maintaining movie metadata.

The v1 product focuses on making the basic viewing loop work end to end: a user can log in, find a movie in the list, and watch it, while an administrator can add and manage the movies that appear there.

## Core Value

Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] Regular users can log in before accessing the movie viewing experience
- [ ] Users can browse a movie list in the web frontend
- [ ] Users can play uploaded movie videos in the browser
- [ ] Administrators can log in to a management area
- [ ] Administrators can upload local video files
- [ ] Administrators can create, edit, and manage movie records shown to users
- [ ] The frontend and backend are separated with a clear API boundary

### Out of Scope

- External video providers - v1 uses administrator-uploaded local video files
- Payment, subscription, and membership tiers - not part of the initial viewing loop
- Native mobile apps - v1 is web-first
- Advanced recommendation algorithms - browsing and playback matter first
- Live streaming - v1 handles uploaded movie files, not live broadcasts

## Context

The project starts from an almost empty repository. The user described the goal as a video/movie web app where films can be watched from the web, with separated frontend and backend. Both ordinary viewers and administrators are in scope.

The confirmed v1 direction:

- Ordinary users need accounts and must log in.
- Administrators upload local video files.
- The main user experience is browsing the movie list and playing movies.
- Admin movie management is part of the initial product, not a later add-on.

## Constraints

- **Architecture**: Frontend and backend must be separated - this is an explicit project requirement.
- **Video source**: v1 movie content comes from administrator-uploaded local video files - external video URLs are out of scope.
- **Authentication**: Regular user login is required for viewing - anonymous viewing is not the initial model.
- **Web-first**: The viewing experience is delivered through a browser - native apps are deferred.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build as separated frontend and backend | Explicit user requirement and a clean fit for web video catalog/API boundaries | Pending |
| Require ordinary user login for viewing | User confirmed login is required | Pending |
| Support administrator-uploaded local videos in v1 | User confirmed uploaded local video files are the source of movie content | Pending |
| Include admin movie management in v1 | User confirmed backend movie management is part of the core scope | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? Move to Out of Scope with reason
2. Requirements validated? Move to Validated with phase reference
3. New requirements emerged? Add to Active
4. Decisions to log? Add to Key Decisions
5. "What This Is" still accurate? Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-29 after initialization*
