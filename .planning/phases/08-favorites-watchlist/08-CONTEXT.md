# Phase 8 Context: Favorites/Watchlist

**Created:** 2026-04-29
**Milestone:** v1.2 Watch History & Favorites
**Requirements:** FAV-01, FAV-02, FAV-03, FAV-04

## Goal

Allow users to save movies to a personal watchlist for later viewing.

## Requirements Mapping

- **FAV-01**: User can add a movie to their favorites/watchlist
- **FAV-02**: User can remove a movie from their favorites/watchlist
- **FAV-03**: User can view their favorites/watchlist in a dedicated page
- **FAV-04**: User can start playback directly from favorites/watchlist

## Existing Codebase Context

### Backend
- FastAPI + SQLAlchemy + SQLite
- JWT authentication in `backend/app/routes/auth.py`
- User routes in `backend/app/routes/user.py`
- Movie model in `backend/app/models/movie.py`
- WatchHistory model pattern established in Phase 7

### Frontend
- React + TypeScript + React Router
- AuthContext for user state
- Catalog page with movie grid
- History page pattern from Phase 7
- Playback page with video player

## Implementation Approach

Follow Phase 7 pattern:
1. Create Favorite model (similar to WatchHistory)
2. Create favorite service with CRUD
3. Add favorite endpoints to user routes
4. Create Favorites page in frontend
5. Add toggle buttons to Catalog and Playback pages
