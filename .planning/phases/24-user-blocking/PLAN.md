# PLAN: Phase 24 - User Blocking

**Milestone:** v1.9 Admin & Safety
**Phase:** 24
**Goal:** Implement user blocking for safety

## Requirements

- BLOCK-01: User can block another user
- BLOCK-02: User can unblock a blocked user
- BLOCK-03: Blocked user's content is hidden from blocker
- BLOCK-04: Blocked user cannot comment on blocker's reviews
- BLOCK-05: User can view their blocked users list

## Success Criteria

1. User can block/unblock from profile page
2. Blocked users' content is filtered from view
3. Blocked users cannot interact with blocker's content
4. User can manage their blocked list
5. Block status is symmetric (blocking hides both directions)

## Implementation Plan

### Task 1: Backend - UserBlock Model
- Create UserBlock model with blocker_id, blocked_id, created_at
- Unique constraint on (blocker_id, blocked_id)
- Prevent self-blocking

### Task 2: Backend - Block API
- POST /api/users/{id}/block - Block user
- DELETE /api/users/{id}/block - Unblock user
- GET /api/users/blocked - List blocked users
- GET /api/users/{id}/block/status - Check if blocked

### Task 3: Backend - Content Filtering
- Filter blocked users' reviews from catalog
- Filter blocked users' comments from reviews
- Filter blocked users from activity feed
- Check block status before allowing comments

### Task 4: Backend - Interaction Prevention
- Prevent blocked users from commenting on blocker's reviews
- Prevent blocked users from following blocker
- Check block relationship in both directions

### Task 5: Frontend - Block Button
- Add block button to user profiles
- Block/unblock toggle
- Confirmation dialog
- Success feedback

### Task 6: Frontend - Blocked Users Page
- Create /settings/blocked route
- List of blocked users with unblock option
- Empty state messaging

## Dependencies

- Existing User model
- Existing follow system
- Existing comment system

## Risks

- Performance: Check block status in many queries
- Consider caching block relationships

---
*Phase plan created: 2026-04-30*
