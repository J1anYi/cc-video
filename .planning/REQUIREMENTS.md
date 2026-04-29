# Requirements: CC Video

**Defined:** 2026-04-29
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Authentication

- [x] **AUTH-01**: User can log in with valid credentials before accessing movie pages
- [x] **AUTH-02**: User session persists across browser refresh until logout or expiration
- [x] **AUTH-03**: User can log out from the web app
- [x] **AUTH-04**: Administrator access is restricted to users with an admin role

### Movie Catalog

- [x] **CAT-01**: Logged-in user can view a list of published movies
- [x] **CAT-02**: Logged-in user can see movie title, description, and basic metadata in the catalog
- [x] **CAT-03**: Logged-in user can open a movie playback page from the catalog

### Playback

- [x] **PLAY-01**: Logged-in user can play an administrator-uploaded movie in the browser
- [x] **PLAY-02**: Backend serves video files only after access is authorized
- [x] **PLAY-03**: Browser playback supports seeking for uploaded video files where the file format supports it

### Admin Management

- [x] **ADM-01**: Administrator can create a movie record with title, description, and publication status
- [x] **ADM-02**: Administrator can upload a local video file and attach it to a movie record
- [x] **ADM-03**: Administrator can edit movie metadata after creation
- [x] **ADM-04**: Administrator can publish, unpublish, or disable a movie
- [x] **ADM-05**: Administrator can delete or remove a movie from the catalog

### API Architecture

- [x] **API-01**: Frontend communicates with backend through documented HTTP APIs
- [x] **API-02**: Backend persists users, roles, movies, and uploaded video file metadata
- [x] **API-03**: Frontend has separate user-facing and admin-facing routes

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Discovery

- **DISC-01**: User can search movies by title
- **DISC-02**: User can filter movies by category, genre, or tag
- **DISC-03**: User can view watch history

### Media

- **MED-01**: Administrator can upload poster images
- **MED-02**: Administrator can manage subtitles
- **MED-03**: System can transcode videos into web-optimized renditions

### Account

- **ACC-01**: User can register a new account from the public web UI
- **ACC-02**: User can reset password by email

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| External video provider ingestion | v1 uses administrator-uploaded local video files |
| Payment, subscription, or membership tiers | Not part of the confirmed initial viewing loop |
| Native mobile apps | v1 is web-first |
| Recommendations | Browsing and playback are the core v1 value |
| Live streaming | v1 handles uploaded movie files |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 1 | ✅ Complete |
| AUTH-02 | Phase 1 | ✅ Complete |
| AUTH-03 | Phase 1 | ✅ Complete |
| AUTH-04 | Phase 1 | ✅ Complete |
| CAT-01 | Phase 3 | ✅ Complete |
| CAT-02 | Phase 3 | ✅ Complete |
| CAT-03 | Phase 3 | ✅ Complete |
| PLAY-01 | Phase 3 | ✅ Complete |
| PLAY-02 | Phase 3 | ✅ Complete |
| PLAY-03 | Phase 3 | ✅ Complete |
| ADM-01 | Phase 2 | ✅ Complete |
| ADM-02 | Phase 2 | ✅ Complete |
| ADM-03 | Phase 2 | ✅ Complete |
| ADM-04 | Phase 2 | ✅ Complete |
| ADM-05 | Phase 2 | ✅ Complete |
| API-01 | Phase 1 | ✅ Complete |
| API-02 | Phase 1 | ✅ Complete |
| API-03 | Phase 4 | ✅ Complete |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0
- Completed: 18
- Remaining: 0

---
*Requirements defined: 2026-04-29*
*Last updated: 2026-04-29 after Phase 4 completion*
