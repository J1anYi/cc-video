# Requirements: CC Video v1.2

**Defined:** 2026-04-29
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## v1.2 Requirements

Requirements for Watch History & Favorites milestone. Each maps to roadmap phases.

### History

- [x] **HIST-01**: User can view a list of previously watched movies
- [x] **HIST-02**: Watch history shows playback progress for each movie
- [x] **HIST-03**: User can resume playback from where they left off
- [x] **HIST-04**: Watch history is sorted by most recently watched

### Favorites

- [x] **FAV-01**: User can add a movie to their favorites/watchlist
- [x] **FAV-02**: User can remove a movie from their favorites/watchlist
- [x] **FAV-03**: User can view their favorites/watchlist in a dedicated page
- [x] **FAV-04**: User can start playback directly from favorites/watchlist

## v1.1 Requirements (Completed)

All v1.1 requirements satisfied. See `.planning/milestones/v1.1-REQUIREMENTS.md` for archive.

## Future Requirements

Deferred to future releases. Tracked but not in current roadmap.

### Media (Future)

- **MED-01**: Administrator can upload poster images
- **MED-02**: Administrator can manage subtitles
- **MED-03**: System can transcode videos into web-optimized renditions

### Account (Future)

- **ACC-04**: User can reset password by email
- **ACC-05**: User can update profile information

### Discovery (Future)

- **DISC-06**: Personalized recommendations based on watch history

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| External video provider ingestion | v1 uses administrator-uploaded local video files |
| Payment, subscription, or membership tiers | Not part of the confirmed initial viewing loop |
| Native mobile apps | v1 is web-first |
| Recommendations | Requires more user behavior signals first |
| Live streaming | v1 handles uploaded movie files |
| Password reset by email | Deferred to v1.3 - requires email infrastructure |
| Social features (sharing, comments) | Not part of current user journey |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| HIST-01 | Phase 7 | Complete |
| HIST-02 | Phase 7 | Complete |
| HIST-03 | Phase 7 | Complete |
| HIST-04 | Phase 7 | Complete |
| FAV-01 | Phase 8 | Complete |
| FAV-02 | Phase 8 | Complete |
| FAV-03 | Phase 8 | Complete |
| FAV-04 | Phase 8 | Complete |

**Coverage:**
- v1.2 requirements: 8 total
- Mapped to phases: 8
- Unmapped: 0
- Completed: 8
- Remaining: 0

---
*Requirements defined: 2026-04-29 for v1.2 milestone*
