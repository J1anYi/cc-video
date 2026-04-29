# Phase 13 Context: Personalized Recommendations

## Phase Overview

**Goal:** Provide personalized movie recommendations and continue watching functionality

**Requirements:**
- REC-01: Personalized Recommendations
- REC-02: Continue Watching

**Depends on:** Phase 7 (Watch History), Phase 8 (Favorites)

## Existing Context

### Relevant Models
- `WatchHistory` - has `progress` field (0-100), `last_watched_at`
- `Favorite` - user favorites
- `Movie` - has `category` field for genre-based matching

### Existing Services
- `history_service` - manages watch history with progress tracking
- `favorite_service` - manages user favorites

### Key Insight
The `WatchHistory.progress` field already exists and tracks viewing progress. "Continue Watching" can use this directly - just filter for `progress < 100`.

## Technical Approach

### REC-01: Personalized Recommendations
Strategy: Content-based filtering using:
1. Categories from watched movies
2. Categories from favorited movies
3. Rank by: most-watched categories + favorite categories

### REC-02: Continue Watching
Strategy: Use existing `WatchHistory.progress` field:
1. Filter for entries where `progress < 100`
2. Sort by `last_watched_at desc`
3. Return movie with progress for resume position

## Files to Create/Modify

### Backend
- `backend/app/services/recommendation.py` (NEW)
- `backend/app/routes/recommendations.py` (NEW)
- `backend/app/schemas/recommendation.py` (NEW)

### Frontend
- `frontend/src/api/recommendations.ts` (NEW)
- `frontend/src/components/Recommendations.tsx` (NEW)
- `frontend/src/components/ContinueWatching.tsx` (NEW)
- `frontend/src/routes/Catalog.tsx` (MODIFY - add sections)

## Acceptance Criteria

- [ ] GET /recommendations returns personalized picks
- [ ] GET /recommendations/continue-watching returns incomplete movies
- [ ] Recommendations shown on catalog page
- [ ] Continue watching shows progress bar
- [ ] Clicking continue watching resumes from saved position
