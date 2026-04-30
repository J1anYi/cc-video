# PLAN: Phase 18 - Notifications & Profiles

**Milestone:** v1.7 Social Extensions
**Phase:** 18
**Goal:** Implement notification system and enhance social profiles

## Requirements

- NOTIF-01: User receives notification when followed user posts a review
- NOTIF-02: User receives notification when someone replies to their comment
- NOTIF-03: User can mark notifications as read
- NOTIF-04: User can view notification history
- NOTIF-05: Notification badge shows unread count

## Success Criteria

1. Users receive in-app notifications for social events
2. Notification badge displays accurate unread count
3. Users can mark notifications as read individually or all at once
4. Notification history shows all past notifications
5. Notifications link to relevant content (review, comment, user)

## Implementation Plan

### Task 1: Backend - Notification Model
- Create `Notification` model with user_id, type, title, content, is_read, created_at
- Include reference fields: actor_id, target_type, target_id
- Types: new_follower, new_review, comment_reply

### Task 2: Backend - Notification Creation Logic
- Create notification when user follows another user
- Create notification when followed user posts a review
- Create notification when someone replies to a comment
- Batch creation for follower notifications (to avoid spam)

### Task 3: Backend - Notification API Endpoints
- GET /api/notifications - List notifications with pagination
- PATCH /api/notifications/{id}/read - Mark as read
- PATCH /api/notifications/read-all - Mark all as read
- GET /api/notifications/unread-count - Get unread count

### Task 4: Frontend - Notification Bell Component
- Add notification bell to header
- Show unread count badge
- Dropdown with recent notifications
- Click to mark as read and navigate

### Task 5: Frontend - Notifications Page
- Create `/notifications` route
- Show all notifications with pagination
- Filter by read/unread
- Mark all as read button

### Task 6: Frontend - Real-time Updates
- Poll for new notifications periodically (every 30s)
- Update badge count without page refresh
- Show toast for new notifications

### Task 7: Integration Testing
- Test notification creation on follow events
- Test notification creation on review events
- Test notification creation on comment replies
- Test read/unread functionality

## Dependencies

- Phase 17 (User Following system)
- Existing Comment model
- Existing Review model

## Risks

- Notification volume: Consider rate limiting or batching
- Performance: Frequent polling may impact server load
- Consider using WebSocket for real-time updates in future

---
*Phase plan created: 2026-04-30*
