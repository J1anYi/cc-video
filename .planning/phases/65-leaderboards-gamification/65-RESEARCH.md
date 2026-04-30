# Phase 65 Research: Leaderboards & Gamification

## Research Summary

### Points System

**Point Values:**
- Watch movie: 10 points
- Write review: 25 points
- Vote on poll: 5 points
- Complete quiz: 15 points
- Host watch party: 20 points

### Leaderboard Architecture

**Models:**
- UserPoints: user_id, total_points, weekly_points, last_updated
- PointsLog: user_id, activity_type, points, created_at

### Leaderboard Calculation

- All-time: Sum of all points
- Weekly: Points earned in current week
- Rank: Position in sorted list
- Reset weekly on Monday

### API Endpoints

- GET /api/leaderboard - Global leaderboard
- GET /api/leaderboard/weekly - Weekly leaderboard
- GET /api/users/me/rank - User rank

---
*Research completed: 2026-04-30*
