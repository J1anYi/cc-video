# PLAN: Phase 26 - User Analytics Dashboard

**Milestone:** v1.10 Analytics & Insights
**Phase:** 26
**Goal:** Implement personal analytics dashboard for users

## Requirements

- ANALYTICS-01: User can view personal watch statistics (total hours, movies watched)
- ANALYTICS-02: User can view genre preferences breakdown
- ANALYTICS-03: User can view watching patterns by time/day
- ANALYTICS-04: User can see their activity timeline
- ANALYTICS-05: User can export their viewing data

## Success Criteria

1. Users can access analytics dashboard from profile menu
2. Dashboard shows accurate watch time statistics
3. Genre breakdown displays visual chart (pie/bar)
4. Time patterns show hourly and daily viewing trends
5. Activity timeline shows recent viewing history
6. Users can export data as JSON or CSV

## Implementation Plan

### Task 1: Backend - Analytics Data Model
- Create `UserAnalytics` model to cache computed stats
- Create `ViewingSession` model for detailed tracking
- Add aggregation functions for statistics

### Task 2: Backend - Analytics API Endpoints
- GET /api/users/me/analytics - Get all analytics
- GET /api/users/me/analytics/watch-time - Total hours
- GET /api/users/me/analytics/genres - Genre breakdown
- GET /api/users/me/analytics/patterns - Time patterns
- GET /api/users/me/analytics/export - Export data

### Task 3: Backend - Statistics Computation
- Implement watch time calculation from history
- Implement genre preference aggregation
- Implement time pattern analysis (hour/day)
- Cache results with periodic refresh

### Task 4: Frontend - Analytics Dashboard Page
- Create `/profile/analytics` route
- Design dashboard layout with cards
- Implement watch statistics section
- Implement genre breakdown chart

### Task 5: Frontend - Visualizations
- Use chart library (Recharts recommended)
- Pie chart for genre distribution
- Bar chart for time patterns
- Line chart for viewing trends over time

### Task 6: Frontend - Activity Timeline
- Show recent activity with timestamps
- Filter by activity type (watch, rate, review)
- Pagination for history

### Task 7: Data Export Feature
- JSON export endpoint
- CSV export endpoint
- Download button in UI

### Task 8: Integration Testing
- Test analytics accuracy
- Test export functionality
- Test caching behavior

## Dependencies

- Watch history data (v1.2)
- Genre metadata on movies
- Existing user profile system

## Risks

- Performance: Computing stats on large histories
- Mitigation: Cache computed values, background jobs

---
*Phase plan created: 2026-04-30*
