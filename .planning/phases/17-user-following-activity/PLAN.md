# PLAN: Phase 17 - User Following & Activity

**Milestone:** v1.7 Social Extensions
**Phase:** 17
**Goal:** Implement user following system and activity feed

## Requirements

- FOLLOW-01: User can follow another user
- FOLLOW-02: User can unfollow another user
- FOLLOW-03: User can view list of their followers
- FOLLOW-04: User can view list of users they follow
- FOLLOW-05: User can see follower/following count on profiles
- ACTIVITY-01: User can view activity feed from followed users
- ACTIVITY-02: Activity feed shows new reviews from followed users
- ACTIVITY-03: Activity feed shows new ratings from followed users
- ACTIVITY-04: Activity feed is sorted by most recent activity
- PROFILE-01: User can view other users' public profiles
- PROFILE-02: Profile shows user's reviews and ratings
- PROFILE-03: Profile shows follower/following counts
- PROFILE-04: Profile shows favorite movies (if public)

## Success Criteria

1. User can follow/unfollow any user from their profile page
2. User can see their followers and following lists
3. Activity feed displays reviews and ratings from followed users
4. User profiles show public activity (reviews, ratings, favorites)
5. Follower/following counts are accurate and update in real-time

## Implementation Plan

### Task 1: Backend - User Follow Model
- Create `UserFollow` model with follower_id, following_id, created_at
- Add uniqueness constraint on (follower_id, following_id)
- Prevent self-following

### Task 2: Backend - Follow API Endpoints
- POST /api/users/{user_id}/follow - Follow a user
- DELETE /api/users/{user_id}/follow - Unfollow a user
- GET /api/users/{user_id}/followers - List followers
- GET /api/users/{user_id}/following - List following

### Task 3: Backend - Activity Model
- Create `Activity` model to track user actions (review posted, rating added)
- Activities: user_id, activity_type, reference_id, created_at
- Auto-create activities on review/rating creation

### Task 4: Backend - Activity Feed API
- GET /api/feed - Get activity feed from followed users
- Include pagination and sorting by created_at desc
- Return activity type, user info, movie info, and action details

### Task 5: Backend - User Profile API Enhancement
- GET /api/users/{user_id} - Return public profile with stats
- Include: display_name, follower_count, following_count, review_count
- Include recent reviews and ratings

### Task 6: Frontend - User Profile Page
- Create `/users/:userId` route
- Show profile info, stats, follow/unfollow button
- Display user's reviews and ratings
- Show favorite movies

### Task 7: Frontend - Follow/Unfollow UI
- Add follow button to user profiles
- Implement follower/following list modals or pages
- Update counts in real-time after follow actions

### Task 8: Frontend - Activity Feed Page
- Create `/feed` route for activity feed
- Show activities from followed users
- Link to relevant movies, reviews, and user profiles
- Empty state for users not following anyone

## Dependencies

- Existing User model
- Existing Review and Rating models
- Existing Favorite model

## Risks

- Performance: Activity feed queries may need optimization for large follow counts
- Consider caching follower counts

---
*Phase plan created: 2026-04-30*
