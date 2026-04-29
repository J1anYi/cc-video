# Roadmap: CC Video v1.2

**Created:** 2026-04-29
**Granularity:** Coarse
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Overview

| Phase | Name | Goal | Requirements | UI hint |
|-------|------|------|--------------|---------|
| 7 | Watch History | Track and display user viewing history | HIST-01, HIST-02, HIST-03 | yes |
| 8 | Favorites/Watchlist | Allow users to save and manage favorite movies | FAV-01, FAV-02, FAV-03, FAV-04 | yes |

## Phase Details

### Phase 7: Watch History

**Goal:** Enable users to track their viewing history and quickly resume previously watched movies.

**Requirements:** HIST-01, HIST-02, HIST-03

**Success Criteria:**

1. User can view a list of movies they have watched
2. Each history entry shows the movie title and last watched timestamp
3. User can click a history item to navigate to the movie player
4. History is automatically updated when user watches a movie
5. History is private to each user (not visible to others)

**Notes:**

- Backend needs a WatchHistory model (user_id, movie_id, last_watched_at)
- Track progress: record when user starts/continues watching
- Frontend needs a History page/route
- Consider pagination for users with extensive history

### Phase 8: Favorites/Watchlist

**Goal:** Allow users to bookmark movies for later viewing.

**Requirements:** FAV-01, FAV-02, FAV-03, FAV-04

**Success Criteria:**

1. User can add a movie to favorites from catalog or movie detail
2. User can remove a movie from favorites
3. User can view their favorites list on a dedicated page
4. Favorite movies show a visual indicator (heart/star) in catalog
5. Favorites persist across sessions

**Notes:**

- Backend needs a Favorite model (user_id, movie_id, created_at)
- Many-to-many relationship between users and movies
- Frontend needs favorites toggle on movie cards
- Frontend needs a Favorites page/route

## Coverage Validation

| Requirement | Phase | Status |
|-------------|-------|--------|
| HIST-01 | Phase 7 | ⏳ Pending |
| HIST-02 | Phase 7 | ⏳ Pending |
| HIST-03 | Phase 7 | ⏳ Pending |
| FAV-01 | Phase 8 | ⏳ Pending |
| FAV-02 | Phase 8 | ⏳ Pending |
| FAV-03 | Phase 8 | ⏳ Pending |
| FAV-04 | Phase 8 | ⏳ Pending |

**Coverage:**
- v1.2 requirements: 7 total
- Mapped to phases: 7
- Unmapped: 0
- Completed: 0
- Remaining: 7

---
*Roadmap created: 2026-04-29 for v1.2 milestone*
