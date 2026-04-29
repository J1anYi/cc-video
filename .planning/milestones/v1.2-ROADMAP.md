# Roadmap: CC Video

## Milestones

- ✅ **v1.0 MVP** — Phases 1-4 (shipped 2026-04-29)
- ✅ **v1.1 Discovery & Registration** — Phases 5-6 (shipped 2026-04-29)
- 🚧 **v1.2 Watch History & Favorites** — Phases 7-8 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) — SHIPPED 2026-04-29</summary>

- [x] Phase 1: Backend Foundation (5/5 plans)
- [x] Phase 2: Admin Movie Management (2/2 plans)
- [x] Phase 3: User Catalog & Playback (1/1 plan)
- [x] Phase 4: Frontend Integration (1/1 plan)

</details>

<details>
<summary>✅ v1.1 Discovery & Registration (Phases 5-6) — SHIPPED 2026-04-29</summary>

- [x] Phase 5: Movie Search & Filtering (3/3 plans)
- [x] Phase 6: User Registration (1/1 plan)

</details>

### 🚧 v1.2 Watch History & Favorites (In Progress)

- [x] **Phase 7: Watch History** — Track user viewing history with progress ✅ 2026-04-29
- [x] **Phase 8: Favorites/Watchlist** — Allow users to save movies for later ✅ 2026-04-29

## Phase Details

### Phase 7: Watch History

**Goal:** Enable users to track and resume their viewing history.

**Requirements:** HIST-01, HIST-02, HIST-03, HIST-04

**Success Criteria:**

1. User can view a list of previously watched movies in reverse chronological order
2. Each history entry shows the movie title, thumbnail, and progress percentage
3. User can click a history entry to resume playback from where they left off
4. History is automatically updated when user watches a movie

**Notes:**

- Need new `WatchHistory` model to store user-movie-view relationships
- Track playback position for resume functionality
- Consider privacy: history is user-specific, never shared

---

### Phase 8: Favorites/Watchlist

**Goal:** Allow users to save movies to a personal watchlist.

**Requirements:** FAV-01, FAV-02, FAV-03, FAV-04

**Success Criteria:**

1. User can add a movie to favorites from the catalog or playback page
2. User can remove a movie from favorites
3. User can view their favorites list in a dedicated page
4. User can start playback directly from the favorites page

**Notes:**

- Need new `Favorite` model for user-movie relationships
- Toggle button should be easily accessible
- Favorites should be sorted by date added (most recent first)

---

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Backend Foundation | v1.0 | 5/5 | Complete | 2026-04-29 |
| 2. Admin Movie Management | v1.0 | 2/2 | Complete | 2026-04-29 |
| 3. User Catalog & Playback | v1.0 | 1/1 | Complete | 2026-04-29 |
| 4. Frontend Integration | v1.0 | 1/1 | Complete | 2026-04-29 |
| 5. Movie Search & Filtering | v1.1 | 3/3 | Complete | 2026-04-29 |
| 6. User Registration | v1.1 | 1/1 | Complete | 2026-04-29 |
| 7. Watch History | v1.2 | 1/1 | Complete | 2026-04-29 |
| 8. Favorites/Watchlist | v1.2 | 1/1 | Complete | 2026-04-29 |

## Coverage Validation

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
*Last updated: 2026-04-29 for v1.2 milestone*
