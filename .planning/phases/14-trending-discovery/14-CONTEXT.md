# Phase 14 Context: Trending & Discovery

## Phase Overview

**Goal:** Add trending movies and related movies features

**Requirements:**
- REC-03: Trending/Popular Movies
- REC-04: Related Movies

**Depends on:** Phase 13 (Recommendations)

## Technical Approach

### REC-03: Trending Movies
- Track view count per movie (already partially done via watch_history)
- Query movies with most watches in last 7 days
- Show on catalog page (public, no auth required)

### REC-04: Related Movies
- Show movies with same category on movie detail page
- Exclude current movie from results

## Files to Create/Modify

### Backend
- backend/app/services/trending.py (NEW)
- backend/app/routes/trending.py (NEW)
- backend/app/schemas/trending.py (NEW)

### Frontend
- frontend/src/api/trending.ts (NEW)
- frontend/src/components/Trending.tsx (NEW)
- frontend/src/components/RelatedMovies.tsx (NEW)
- frontend/src/routes/Catalog.tsx (MODIFY)
- frontend/src/routes/Playback.tsx (MODIFY)
