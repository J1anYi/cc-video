# CC Video

## What This Is

CC Video is a web-based movie watching system with separated frontend and backend services. Regular users log in, browse a movie catalog, and play uploaded videos in the browser; administrators manage the movie library by uploading local video files and maintaining movie metadata.

The v1 product focuses on making the basic viewing loop work end to end: a user can log in, find a movie in the list, and watch it, while an administrator can add and manage the movies that appear there.

## Current Milestone: v1.3 Media Enhancement

**Goal:** Enhance viewing experience with poster images and subtitle support

**Target features:**
- Poster image upload for movies
- Subtitle management and display
- Improved visual catalog presentation

## Core Value

Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Requirements

### Validated

- [x] Regular users can log in before accessing the movie viewing experience
- [x] Users can browse a movie list in the web frontend
- [x] Users can play uploaded movie videos in the browser
- [x] Administrators can log in to a management area
- [x] Administrators can upload local video files
- [x] Administrators can create, edit, and manage movie records shown to users
- [x] The frontend and backend are separated with a clear API boundary
- [x] User can search movies by title (v1.1)
- [x] User can register a new account from the public web UI (v1.1)
- [x] User can filter movies by category or genre (v1.1)
- [x] User can view watch history (v1.2)
- [x] User can save favorites/watchlist (v1.2)

### Active

- [ ] Administrator can upload poster images
- [ ] Administrator can manage subtitles

### Out of Scope

- External video providers - v1 uses administrator-uploaded local video files
- Payment, subscription, and membership tiers - not part of the initial viewing loop
- Native mobile apps - v1 is web-first
- Advanced recommendation algorithms - browsing and playback matter first
- Live streaming - v1 handles uploaded movie files, not live broadcasts
- Password reset by email - deferred to v1.4
- Subtitles and multiple audio tracks - deferred to v1.4+

## Context

v1.0 MVP completed successfully with all 18 requirements satisfied. The core viewing loop (admin upload → user catalog → user playback) works end-to-end.

v1.1 added search, filtering, and user self-registration - enabling discoverability and organic user growth.

v1.2 added watch history and favorites - increasing user engagement and retention.

v1.3 focuses on media enhancement:
1. **Poster Images** - Visual movie cards with cover art
2. **Subtitles** - Accessibility and multi-language support

## Constraints

- **Architecture**: Frontend and backend must be separated - this is an explicit project requirement.
- **Video source**: v1 movie content comes from administrator-uploaded local video files - external video URLs are out of scope.
- **Authentication**: Regular user login is required for viewing - anonymous viewing is not the initial model.
- **Web-first**: The viewing experience is delivered through a browser - native apps are deferred.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Build as separated frontend and backend | Explicit user requirement and a clean fit for web video catalog/API boundaries | Validated |
| Require ordinary user login for viewing | User confirmed login is required | Validated |
| Support administrator-uploaded local videos in v1 | User confirmed uploaded local video files are the source of movie content | Validated |
| Include admin movie management in v1 | User confirmed backend movie management is part of the core scope | Validated |
| Add search before advanced discovery features | Search is table stakes for any catalog; filtering can follow | Validated |
| Add self-registration before password reset | Registration enables organic growth; password reset is support for existing users | Validated |
| Add watch history before recommendations | History is personal data; recommendations require more signals | Validated |
| Add favorites before watch history | Favorites are explicit user intent; history is passive | Validated |
| Add poster images before subtitles | Visual catalog first; accessibility enhancement follows | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? Move to Out of Scope with reason
2. Requirements validated? Move to Validated with phase reference
3. New requirements emerged? Add to Active
4. Decisions to log? Add to Key Decisions
5. "What This Is" still accurate? Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-29 starting v1.3 milestone*
