# Phase 7 Context: Watch History

## Context Gathering Date: 2026-04-29

## Phase Goal

Enable users to track and resume their viewing history.

**Requirements:** HIST-01, HIST-02, HIST-03, HIST-04

## Decisions

### Data Model

**Decision:** Create WatchHistory model with user_id, movie_id, progress, last_watched_at

**Rationale:**
- Simple relationship model tracking user-movie viewing
- Progress stored as percentage (0-100)
- Timestamp for sorting by most recent

**Implementation:**
- New model in backend/app/models/watch_history.py
- Foreign keys to User and Movie
- Unique constraint on (user_id, movie_id) - one entry per movie per user

### Progress Tracking

**Decision:** Track progress as integer percentage (0-100)

**Rationale:**
- Video duration varies; percentage is duration-agnostic
- Easy to calculate resume position: duration * (progress / 100)
- Frontend already has video duration from playback

**Implementation:**
- Backend receives progress percentage from frontend
- Frontend sends progress on pause/end/interval events
- Calculate resume time: video.duration * (history.progress / 100)

### History Updates

**Decision:** Update history on playback events (play, pause, end)

**Rationale:**
- Accurate tracking requires periodic updates
- Do not need real-time - update at key events is sufficient
- Simpler implementation than continuous polling

**Implementation:**
- POST /history endpoint to create/update entry
- Frontend sends update when:
  - User pauses video
  - Video ends (progress = 100)
  - User leaves playback page (beforeunload event)

### History Display

**Decision:** Show history in reverse chronological order with progress bar

**Rationale:**
- Users expect most recent first
- Visual progress indicator helps resume decision
- Thumbnail + title + progress provides enough context

**Implementation:**
- New History page at /history route
- Movie cards show progress bar overlay
- Click navigates to /movies/:id with auto-resume

### Resume Playback

**Decision:** Auto-resume from saved position when user plays from history

**Rationale:**
- Expected behavior for video streaming services
- Requires passing start time to video player
- User can always seek to beginning if desired

**Implementation:**
- Playback page accepts ?t= query param for start time
- Video player seeks to time on load if param present
- History link includes calculated start time

## Code Context

### Reusable Assets

1. Backend User/Movie Models - Already exist with relationships
2. Auth System - JWT-based, user_id available in routes
3. Movie Service - Can extend with history queries
4. Frontend Video Player - Already has seek functionality

### Gaps to Fill

1. Backend:
   - Create WatchHistory model
   - Create history service with CRUD operations
   - Add history endpoints (list, update)

2. Frontend:
   - Create History page component
   - Add progress tracking to Playback component
   - Add /history route
   - Add History navigation link

### File Changes Expected

Backend:
- backend/app/models/watch_history.py - New model
- backend/app/services/history.py - New service
- backend/app/routes/user.py - Add history endpoints

Frontend:
- frontend/src/routes/History.tsx - New page
- frontend/src/routes/Playback.tsx - Add progress tracking
- frontend/src/api/history.ts - New API functions
- frontend/src/api/types.ts - Add WatchHistory type
- frontend/src/App.tsx - Add /history route

## Success Criteria Mapping

| Criterion | Implementation |
|-----------|----------------|
| View list of watched movies | GET /history endpoint + History.tsx |
| Show progress percentage | Progress bar in history cards |
| Resume from saved position | ?t= query param + video seek |
| Sort by most recent | ORDER BY last_watched_at DESC |

## Notes

- Consider cleanup: delete history entries when movie is deleted
- Consider privacy: history is personal, never shared
- Consider performance: index on (user_id, last_watched_at)
