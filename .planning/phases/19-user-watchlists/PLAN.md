# PLAN: Phase 19 - User Watchlists

**Milestone:** v1.8 Content Organization
**Phase:** 19
**Goal:** Implement user watchlists for organizing movies into themed lists

## Requirements

- WATCHLIST-01: User can create a themed watchlist
- WATCHLIST-02: User can add movies to their watchlist
- WATCHLIST-03: User can remove movies from their watchlist
- WATCHLIST-04: User can set watchlist as public or private
- WATCHLIST-05: User can view their own watchlists

## Success Criteria

1. User can create a watchlist with name and description
2. User can add/remove movies from their watchlists
3. User can set privacy settings on watchlists
4. User can view all their watchlists with movie count
5. Watchlist detail view shows all movies in the list

## Implementation Plan

### Task 1: Backend - Watchlist Model
- Create `Watchlist` model with id, user_id, name, description, is_public, created_at
- Create `WatchlistItem` model linking watchlist to movies
- Add unique constraint on (watchlist_id, movie_id)

### Task 2: Backend - Watchlist API Endpoints
- POST /api/watchlists - Create new watchlist
- GET /api/watchlists - List user's watchlists
- GET /api/watchlists/{id} - Get watchlist with movies
- PATCH /api/watchlists/{id} - Update watchlist details
- DELETE /api/watchlists/{id} - Delete watchlist

### Task 3: Backend - Watchlist Items API
- POST /api/watchlists/{id}/movies - Add movie to watchlist
- DELETE /api/watchlists/{id}/movies/{movie_id} - Remove movie from watchlist
- POST /api/watchlists/{id}/movies/batch - Add multiple movies at once

### Task 4: Frontend - Watchlist Page
- Create `/watchlists` route to show user's watchlists
- Create watchlist card component with stats
- Add create watchlist button and modal

### Task 5: Frontend - Watchlist Detail Page
- Create `/watchlists/:id` route for watchlist detail
- Show movie grid with remove option
- Edit watchlist settings button

### Task 6: Frontend - Add to Watchlist UI
- Add "Add to Watchlist" button on movie cards
- Show watchlist selection dropdown
- Show success/error feedback

### Task 7: Frontend - Watchlist Management
- Create/edit watchlist modal
- Privacy toggle switch
- Delete confirmation dialog

## Dependencies

- Existing Movie model
- Existing User model
- Existing Favorite model (pattern to follow)

## Risks

- Performance: Large watchlists may need pagination
- Consider caching watchlist counts

---
*Phase plan created: 2026-04-30*
