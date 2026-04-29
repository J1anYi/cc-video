# PLAN: Phase 27 - Content Performance Metrics

**Milestone:** v1.10 Analytics & Insights
**Phase:** 27
**Goal:** Implement content performance analytics for administrators

## Requirements

- METRICS-01: Admin can view movie engagement statistics
- METRICS-02: Admin can view platform-wide viewing trends
- METRICS-03: Admin can see top performing content
- METRICS-04: Admin can view user retention metrics
- METRICS-05: Admin can access content popularity rankings

## Success Criteria

1. Admin can access metrics dashboard
2. Movie detail pages show engagement stats
3. Platform trends show viewing over time
4. Top content ranking is accurate and sortable
5. Retention metrics show user return rates

## Implementation Plan

### Task 1: Backend - Content Metrics Model
- Create `ContentMetrics` model for movie stats
- Fields: views, unique_viewers, avg_watch_time, completion_rate
- Create `PlatformMetrics` model for aggregated data

### Task 2: Backend - Metrics Computation
- Track movie view events
- Calculate engagement scores
- Compute retention cohorts
- Schedule periodic aggregation jobs

### Task 3: Backend - Admin Metrics API
- GET /api/admin/metrics/overview - Platform summary
- GET /api/admin/metrics/movies/{id} - Movie performance
- GET /api/admin/metrics/trending - Top content
- GET /api/admin/metrics/retention - Retention data
- GET /api/admin/metrics/rankings - Content rankings

### Task 4: Frontend - Admin Metrics Dashboard
- Create `/admin/metrics` route
- Overview cards (total views, users, engagement)
- Trending content list
- Retention chart

### Task 5: Frontend - Movie Performance Page
- Add metrics tab to movie detail (admin)
- View count and trend
- Engagement metrics
- Viewer demographics placeholder

### Task 6: Frontend - Content Rankings
- Sortable table of top movies
- Filter by time period (week, month, all)
- Filter by category

### Task 7: Integration Testing
- Test metrics accuracy
- Test aggregation jobs
- Test admin access control

## Dependencies

- Watch history data
- Admin authentication system
- Content moderation (for context)

## Risks

- Data volume: Large datasets may slow queries
- Mitigation: Use indexed columns, pagination, caching

---
*Phase plan created: 2026-04-30*
