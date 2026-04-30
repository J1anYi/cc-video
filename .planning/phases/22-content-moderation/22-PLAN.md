# PLAN: Phase 22 - Content Moderation

**Milestone:** v1.9 Admin & Safety
**Phase:** 22
**Created:** 2026-04-30

## Goal

Implement content moderation system allowing users to report inappropriate content and admins to review and act on reports.

## Requirements

- **MOD-01**: User can report reviews for inappropriate content
- **MOD-02**: User can report comments for inappropriate content
- **MOD-03**: Admin can view reported content queue
- **MOD-04**: Admin can dismiss reports (content is acceptable)
- **MOD-05**: Admin can remove reported content
- **MOD-06**: Admin can issue warnings to users

## Context

- Existing review and comment models
- Admin panel already has user management
- Need new Report model to track reports
- Need admin interface to manage reports
- Warnings should be tracked on user profile

## Implementation Plan

### Task 1: Backend - Report Model

**File:** `backend/app/models/report.py`

Create Report model:
- id, reporter_id, content_type, content_id, reason, status
- content_type: 'review' | 'comment'
- status: 'pending' | 'dismissed' | 'actioned'
- created_at timestamp

**File:** `backend/app/models/user.py`
- Add `warnings_count` field

### Task 2: Backend - Report Service

**File:** `backend/app/services/report.py`

Implement service methods:
- `create_report(reporter_id, content_type, content_id, reason)`
- `get_pending_reports(page, limit)`
- `dismiss_report(report_id)`
- `action_report(report_id, remove_content, warn_user)`
- `get_report_stats()`

### Task 3: Backend - Report Routes

**File:** `backend/app/routes/reports.py`

Create endpoints:
- POST /api/reports - Report content
- GET /api/admin/reports - List pending reports
- PATCH /api/admin/reports/{id}/dismiss - Dismiss report
- PATCH /api/admin/reports/{id}/action - Take action (remove/warn)

### Task 4: Frontend - Report Modal

**File:** `frontend/src/components/ReportModal.tsx`

Create report modal component:
- Report reason textarea
- Submit button
- Used in review and comment cards

### Task 5: Frontend - Admin Reports Page

**File:** `frontend/src/routes/admin/Reports.tsx`

Admin reports management page:
- Pending reports list
- Report details (reporter, content, reason)
- Dismiss/Action buttons
- Warning toggle

### Task 6: Frontend - Reports API Client

**File:** `frontend/src/api/reports.ts`

API client methods:
- `createReport(contentType, contentId, reason)`
- `getPendingReports(page, limit)`
- `dismissReport(reportId)`
- `actionReport(reportId, removeContent, warnUser)`

## Dependencies

- Phase 15: Ratings & Reviews (Review model)
- Phase 16: Comments & Engagement (Comment model)
- Phase 21: Admin User Management (Admin infrastructure)

## Verification Criteria

- [ ] User can report a review
- [ ] User can report a comment
- [ ] Admin can view list of pending reports
- [ ] Admin can dismiss a report (content stays)
- [ ] Admin can remove reported content
- [ ] Admin can issue warning to user
- [ ] Reported content shows report count
- [ ] User's warning count is tracked

## Files Changed

### Created
- backend/app/models/report.py
- backend/app/services/report.py
- backend/app/routes/reports.py
- frontend/src/api/reports.ts
- frontend/src/components/ReportModal.tsx
- frontend/src/routes/admin/Reports.tsx

### Modified
- backend/app/models/user.py
- backend/app/models/__init__.py
- backend/app/main.py
- frontend/src/App.tsx

---
*Plan created: 2026-04-30*
