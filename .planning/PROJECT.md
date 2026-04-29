# CC Video

## What This Is

CC Video is a web-based movie watching system with separated frontend and backend services. Regular users log in, browse a movie catalog, and play uploaded videos in the browser; administrators manage the movie library by uploading local video files and maintaining movie metadata.

The v1 product focuses on making the basic viewing loop work end to end: a user can log in, find a movie in the list, and watch it, while an administrator can add and manage the movies that appear there.

## Current State: v1.9 Planning (2026-04-30)

**v1.8 Content Organization shipped.** Planning v1.9 Admin & Safety.

The system now supports:
- User authentication with password reset
- Movie browsing, search, and filtering
- Video playback with subtitles and poster images
- Watch history and favorites
- User profile management
- Personalized recommendations
- Continue watching
- Trending movies
- Related movies
- Movie ratings and reviews
- Comments on reviews
- Helpful votes on reviews
- User following system
- Activity feed
- Notifications
- Social profiles
- User watchlists (public/private)
- Public watchlist discovery
- Auto-notifications for social events

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
- [x] Administrator can upload poster images (v1.3)
- [x] Administrator can manage subtitles (v1.3)
- [x] User can reset password by email (v1.4)
- [x] User can update profile information (v1.4)
- [x] User receives personalized recommendations (v1.5)
- [x] User can continue watching from saved position (v1.5)
- [x] User can discover trending movies (v1.5)
- [x] User can view related movies (v1.5)

### Validated (v1.6-v1.8)

- [x] User can rate and review movies — v1.6
- [x] User can comment on reviews — v1.6
- [x] User can mark reviews as helpful — v1.6
- [x] User can follow other users — v1.7
- [x] User can view activity feed — v1.7
- [x] User receives notifications — v1.7
- [x] User can create themed watchlists — v1.8
- [x] User can add/remove movies from watchlists — v1.8
- [x] User can set watchlist privacy — v1.8
- [x] User can browse public watchlists — v1.8
- [x] Auto-notifications for social events — v1.8

### Active

(None - all planned requirements satisfied)

## Current Milestone: v1.9 Admin & Safety

**Goal:** Implement admin user management, content moderation, and advanced search

**Target features:**
- Admin user management dashboard (list, search, suspend users)
- Content moderation tools (reported content queue)
- Advanced search filters (rating, year, duration)
- User blocking system
- @mentions in comments and reviews

### Out of Scope

- External video providers - v1 uses administrator-uploaded local video files
- Payment, subscription, and membership tiers - not part of the initial viewing loop
- Native mobile apps - v1 is web-first
- Advanced recommendation algorithms - browsing and playback matter first
- Live streaming - v1 handles uploaded movie files, not live broadcasts

## Context

v1.0 MVP completed successfully with all 18 requirements satisfied. The core viewing loop (admin upload - user catalog - user playback) works end-to-end.

v1.1 added search, filtering, and user self-registration - enabling discoverability and organic user growth.

v1.2 added watch history and favorites - increasing user engagement and retention.

v1.3 added poster images and subtitles - enhancing visual presentation and accessibility.

v1.4 added password reset and profile management - improving account security and user control.

v1.5 added personalized recommendations, continue watching, trending movies, and related movies - enhancing content discovery.

v1.6 added ratings, reviews, comments, and helpful votes - enabling user engagement and social interaction.

v1.7 added user following, activity feed, notifications, and social profiles - completing the social foundation.

v1.8 added user watchlists, public watchlist discovery, and notification automation - completing content organization.

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
| Add poster images before subtitles | Visual catalog first; accessibility enhancement follows | Validated |
| Use SHA-256 hash for reset tokens | Secure, no plaintext tokens stored | Validated |
| 1-hour token expiration | Balance security and usability | Validated |
| No email enumeration | Prevent account discovery attacks | Validated |
| Content-based filtering by category | Simple, effective, no ML needed | Validated |
| 7-day window for trending | Balance freshness with data volume | Validated |
| Hide recommendations when filters active | User intent is search, not discovery | Validated |

## Evolution

This document evolves at phase transitions and milestone boundaries.

---
*Last updated: 2026-04-30 - v1.9 planning started*
