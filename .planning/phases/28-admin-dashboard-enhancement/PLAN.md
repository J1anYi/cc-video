# PLAN: Phase 28 - Admin Dashboard Enhancement

**Milestone:** v1.10 Analytics & Insights
**Phase:** 28
**Goal:** Enhance admin dashboard with comprehensive platform overview

## Requirements

- DASHBOARD-01: Admin dashboard shows key platform metrics
- DASHBOARD-02: Admin can view recent activity summary
- DASHBOARD-03: Admin can see user growth trends
- DASHBOARD-04: Admin can view content health indicators
- DASHBOARD-05: Admin can access quick action shortcuts

## Success Criteria

1. Dashboard loads with key metrics at a glance
2. Activity feed shows recent platform events
3. User growth chart displays trend over time
4. Content health shows moderation queue, reports
5. Quick actions enable common admin tasks

## Implementation Plan

### Task 1: Backend - Dashboard Data API
- GET /api/admin/dashboard - All dashboard data
- Include: metrics, activity, growth, health
- Optimize for single request response

### Task 2: Backend - Activity Summary
- Track recent admin-relevant events
- User registrations
- Content reports
- New reviews/comments
- Return last 20 activities

### Task 3: Backend - User Growth Tracking
- Track daily user counts
- Calculate growth rate
- Compare to previous periods

### Task 4: Backend - Content Health Indicators
- Count pending reports
- Count unmoderated content
- Flag stale content (no views)
- Content quality score

### Task 5: Frontend - Dashboard Layout
- Redesign admin home page
- Metric cards row (users, movies, views, reports)
- Activity feed sidebar
- Charts section

### Task 6: Frontend - Metric Cards
- Total users with growth indicator
- Total movies with recent additions
- Platform views (today/week)
- Pending reports count

### Task 7: Frontend - Activity Feed
- Real-time activity log
- Filter by event type
- Click to view details
- Timestamp display

### Task 8: Frontend - Quick Actions
- Suspend user shortcut
- Remove content shortcut
- Add movie shortcut
- View reports shortcut

### Task 9: Integration Testing
- Test dashboard data accuracy
- Test activity tracking
- Test quick action links

## Dependencies

- Admin user management (Phase 21)
- Content moderation (Phase 22)
- Content metrics (Phase 27)

## Risks

- Dashboard load time with many metrics
- Mitigation: Async loading, caching, pagination

---
*Phase plan created: 2026-04-30*
