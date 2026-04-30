# PLAN: Phase 22 - Content Moderation

**Milestone:** v1.9 Admin & Safety
**Phase:** 22
**Goal:** Implement content reporting and moderation system

## Requirements

- MOD-01: User can report reviews for inappropriate content
- MOD-02: User can report comments for inappropriate content
- MOD-03: Admin can view reported content queue
- MOD-04: Admin can dismiss reports (content is acceptable)
- MOD-05: Admin can remove reported content
- MOD-06: Admin can issue warnings to users

## Success Criteria

1. Users can report reviews and comments
2. Admin can view all reports in a queue
3. Admin can dismiss or action reports
4. Removed content is no longer visible
5. Warning system notifies users

## Implementation Plan

### Task 1: Backend - Report Model
- Create Report model with reporter_id, content_type, content_id, reason, status
- Status: pending, dismissed, actioned
- Add unique constraint on (reporter_id, content_type, content_id)

### Task 2: Backend - Report API
- POST /api/reports - Create report (review or comment)
- GET /api/admin/reports - List pending reports
- PATCH /api/admin/reports/{id}/dismiss - Dismiss report
- PATCH /api/admin/reports/{id}/action - Action report (remove content)

### Task 3: Backend - Content Removal
- Add is_removed flag to Review and Comment models
- Add removed_at and removed_reason fields
- Filter removed content from queries

### Task 4: Backend - Warning System
- Create UserWarning model with user_id, reason, created_at
- Add warnings endpoint to admin routes
- Notify user of warning

### Task 5: Frontend - Report Button
- Add report button to reviews and comments
- Report reason dropdown (spam, inappropriate, other)
- Success feedback

### Task 6: Frontend - Admin Reports Queue
- Create /admin/reports route
- Table of pending reports with content preview
- Dismiss and action buttons
- Warning dialog for repeat offenders

## Dependencies

- Existing Review model
- Existing Comment model
- Existing admin routes

## Risks

- Report spam: Consider rate limiting
- False reports: Dismiss option handles this

---
*Phase plan created: 2026-04-30*
