# PLAN: Phase 20 - Notification Integration

**Milestone:** v1.8 Content Organization
**Phase:** 20
**Goal:** Complete notification automation and enhance activity feed

## Requirements

- DISCOVER-01: User can browse public watchlists
- DISCOVER-02: User can view watchlist details (owner, movies, title)
- DISCOVER-03: User can follow a watchlist
- NOTIF-AUTO-01: Notification created when followed user posts a review
- NOTIF-AUTO-02: Notification created when someone replies to user's comment
- NOTIF-AUTO-03: Notification created when user gains a new follower
- ACTIVITY-ENH-01: Activity shows when user adds a movie to favorites
- ACTIVITY-ENH-02: Activity shows when user creates a new watchlist

## Success Criteria

1. Notifications are automatically created for social events
2. Activity feed shows favorites and watchlist activities
3. Users can discover and browse public watchlists
4. All notification types include relevant context and links
5. Activity feed is richer with more event types

## Implementation Plan

### Task 1: Backend - Watchlist Discovery API
- GET /api/watchlists/public - Browse all public watchlists
- GET /api/watchlists/{id}/public - Get public watchlist details
- GET /api/users/{id}/watchlists - Get user's public watchlists

### Task 2: Backend - Watchlist Follow System
- Create `WatchlistFollow` model for following watchlists
- POST /api/watchlists/{id}/follow - Follow a watchlist
- DELETE /api/watchlists/{id}/follow - Unfollow a watchlist
- GET /api/watchlists/followed - Get followed watchlists

### Task 3: Backend - Notification Automation
- Hook into ReviewService to create NEW_REVIEW notifications for followers
- Hook into CommentService to create COMMENT_REPLY notifications
- Hook into FollowService to create NEW_FOLLOWER notifications
- Ensure notification includes actor, target, and context

### Task 4: Backend - Activity Enhancements
- Add FAVORITE_ADDED activity type
- Add WATCHLIST_CREATED activity type
- Hook into FavoriteService to create activities
- Hook into WatchlistService to create activities

### Task 5: Frontend - Watchlist Discovery
- Create `/discover/watchlists` route
- Show grid of public watchlists with stats
- Filter by most popular, recent, etc.

### Task 6: Frontend - Public Watchlist View
- Create `/watchlists/:id/public` route for non-owners
- Show watchlist info and movie grid
- Follow/unfollow button

### Task 7: Testing - Notification Flow
- Test follower gets notification on new review
- Test review author gets notification on comment reply
- Test user gets notification on new follower
- Verify notification links work correctly

## Dependencies

- Phase 19 (Watchlist model and routes)
- Existing Notification model and service
- Existing Activity model and service
- Existing Follow relationships

## Risks

- Notification spam: Consider batching or rate limiting
- Performance: Activity feed queries with more event types

---
*Phase plan created: 2026-04-30*
