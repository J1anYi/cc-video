# Requirements: CC Video v1.1

**Defined:** 2026-04-29
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## v1.1 Requirements

Requirements for Discovery & Registration milestone. Each maps to roadmap phases.

### Discovery

- [x] **DISC-01**: User can search movies by title with real-time or submit-based filtering
- [x] **DISC-02**: User can filter movies by category or genre tag
- [x] **DISC-03**: Search and filter results update the catalog view dynamically

### Account

- [x] **ACC-01**: User can register a new account from the public web UI
- [x] **ACC-02**: Registration form validates username uniqueness and password strength
- [x] **ACC-03**: Newly registered users can immediately log in with their credentials

## v1 Requirements (Completed)

All v1 requirements satisfied. See `.planning/milestones/v1.0-REQUIREMENTS.md` for archive.

## Future Requirements

Deferred to future releases. Tracked but not in current roadmap.

### Discovery (Future)

- **DISC-04**: User can view watch history
- **DISC-05**: User can save favorites/watchlist

### Media (Future)

- **MED-01**: Administrator can upload poster images
- **MED-02**: Administrator can manage subtitles
- **MED-03**: System can transcode videos into web-optimized renditions

### Account (Future)

- **ACC-04**: User can reset password by email
- **ACC-05**: User can update profile information

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| External video provider ingestion | v1 uses administrator-uploaded local video files |
| Payment, subscription, or membership tiers | Not part of the confirmed initial viewing loop |
| Native mobile apps | v1 is web-first |
| Recommendations | Browsing and playback are the core v1 value |
| Live streaming | v1 handles uploaded movie files |
| Password reset by email | Deferred to v1.2 - requires email infrastructure |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DISC-01 | Phase 5 | ✅ Complete |
| DISC-02 | Phase 5 | ✅ Complete |
| DISC-03 | Phase 5 | ✅ Complete |
| ACC-01 | Phase 6 | ✅ Complete |
| ACC-02 | Phase 6 | ✅ Complete |
| ACC-03 | Phase 6 | ✅ Complete |

**Coverage:**
- v1.1 requirements: 6 total
- Mapped to phases: 6
- Unmapped: 0
- Completed: 6
- Remaining: 0

---
*Requirements defined: 2026-04-29 for v1.1 milestone*
*All requirements complete: 2026-04-29*
