# PLAN: Phase 29 - Social Analytics

**Milestone:** v1.10 Analytics & Insights
**Phase:** 29
**Goal:** Implement social influence and engagement analytics for users

## Requirements

- SOCIAL-01: User can view their social influence score
- SOCIAL-02: User can see review impact (views, helpful votes)
- SOCIAL-03: User can view follower growth over time
- SOCIAL-04: User can see most engaging content they created
- SOCIAL-05: User can compare their stats with friends

## Success Criteria

1. Social analytics accessible from profile
2. Influence score visible and explained
3. Review performance metrics accurate
4. Follower growth chart displays trend
5. Engaging content ranking works
6. Friend comparison available (opt-in)

## Implementation Plan

### Task 1: Backend - Social Metrics Model
- Create `UserSocialMetrics` model
- Fields: influence_score, follower_count, review_views, helpful_votes
- Create `FollowerHistory` for growth tracking

### Task 2: Backend - Influence Score Calculation
- Define scoring algorithm
- Factors: followers, reviews, helpful votes, engagement
- Calculate and cache score
- Update on relevant events

### Task 3: Backend - Social Analytics API
- GET /api/users/me/social-analytics - All social data
- GET /api/users/me/social-analytics/influence - Score breakdown
- GET /api/users/me/social-analytics/reviews - Review performance
- GET /api/users/me/social-analytics/followers - Growth data
- GET /api/users/me/social-analytics/compare/{userId} - Compare with friend

### Task 4: Backend - Review Impact Tracking
- Track review view counts
- Aggregate helpful votes
- Calculate review engagement rate

### Task 5: Frontend - Social Analytics Page
- Create `/profile/social` route
- Influence score card with breakdown
- Follower growth chart
- Review performance table

### Task 6: Frontend - Influence Score Display
- Visual score indicator (gauge/progress)
- Score breakdown tooltip
- Badge/level system (optional)

### Task 7: Frontend - Follower Growth Chart
- Line chart over time
- Highlight milestones
- Compare to friends (opt-in)

### Task 8: Frontend - Review Performance
- Table of user's reviews
- Columns: movie, views, helpful votes, engagement
- Sort by performance

### Task 9: Friend Comparison Feature
- Select friend to compare
- Side-by-side stats
- Privacy: opt-in for comparison

### Task 10: Integration Testing
- Test influence score calculation
- Test follower tracking
- Test comparison feature

## Dependencies

- User following system (Phase 17)
- Reviews and helpful votes (Phase 15)
- User profile system

## Risks

- Influence gaming: Users may try to game scores
- Mitigation: Rate limits, anti-gaming measures
- Privacy: Comparison should be opt-in

---
*Phase plan created: 2026-04-30*
