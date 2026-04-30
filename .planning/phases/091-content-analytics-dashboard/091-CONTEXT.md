# Phase 91: Content Analytics Dashboard - Context

**Gathered:** 2026-04-30
**Status:** Ready for planning
**Source:** Requirements analysis + existing codebase research

<domain>
## Phase Boundary

Implement advanced content performance analytics for administrators and content managers.
This is **content-centric** analytics (how movies/videos perform) vs existing user-centric analytics (individual viewing habits).

**Delivers:**
- Real-time content performance metrics (views, engagement, completion rates)
- Content engagement heatmaps (where users pause/rewind/abandon)
- View completion analysis (drop-off points, completion rates)
- Content comparison reports (A vs B performance)
- Trending content analysis (velocity, momentum)

**NOT in scope:**
- User analytics (already exists in user_analytics.py)
- Revenue analytics (Phase 93)
- Predictive analytics (Phase 94)

</domain>

<decisions>
## Implementation Decisions

### Data Model
- **ContentAnalytics model**: Store per-content metrics (views, unique_viewers, avg_completion_pct, total_watch_time)
- **ContentEngagementHeatmap model**: Store second-by-second engagement data (timestamp, events)
- **ContentViewSession model**: Track individual viewing sessions for completion analysis

### API Endpoints
- `GET /admin/content/{content_id}/analytics` - Content performance metrics
- `GET /admin/content/{content_id}/heatmap` - Engagement heatmap data
- `GET /admin/content/{content_id}/completion` - Completion analysis
- `POST /admin/content/compare` - Compare multiple content items
- `GET /admin/content/trending` - Trending content with velocity metrics

### Real-time Metrics
- Use cached aggregations refreshed every 5 minutes
- Track view events via viewing_sessions table (already exists)
- Compute completion rate from watch_history.completed flag

### Heatmap Generation
- Sample viewing sessions at 10-second intervals
- Track: play, pause, seek, rewind events per timestamp
- Aggregate into percentage-based heatmap (0-100% engagement at each point)

### Trending Algorithm
- Velocity: views in last 24h vs previous 24h
- Momentum: acceleration of velocity (is it accelerating or decelerating)
- Score = velocity * momentum * quality_factor

### Frontend Components
- ContentAnalyticsDashboard: Main dashboard with metrics cards
- EngagementHeatmap: Visual heatmap component (canvas-based)
- CompletionChart: Line chart showing drop-off curve
- ContentComparisonTable: Side-by-side comparison
- TrendingList: Trending content with velocity indicators

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Analytics Infrastructure
- `backend/app/models/user_analytics.py` — Existing UserAnalytics model pattern
- `backend/app/services/analytics.py` — AnalyticsService pattern for caching/computing
- `backend/app/routes/analytics.py` — Existing analytics route patterns
- `backend/app/schemas/analytics.py` — Existing analytics schemas
- `frontend/src/api/analytics.ts` — Frontend analytics API pattern

### Data Sources
- `backend/app/models/watch_history.py` — WatchHistory model (completion data)
- `backend/app/models/viewing_session.py` — ViewingSession model (session tracking)
- `backend/app/models/movie.py` — Movie model (content items)

</canonical_refs>

<specifics>
## Specific Ideas

### Metrics to Track
1. **Total Views**: Count of all viewing sessions
2. **Unique Viewers**: Distinct users who watched
3. **Average Completion %**: Mean of completion percentages
4. **Total Watch Time**: Sum of all watch durations
5. **Engagement Score**: Weighted metric combining completion + interactions

### Heatmap Structure
```json
{
  "content_id": 123,
  "duration_seconds": 7200,
  "samples": [
    {"timestamp": 0, "engagement": 100, "events": {"play": 150, "pause": 5}},
    {"timestamp": 10, "engagement": 98, "events": {"play": 0, "pause": 3}},
    ...
  ]
}
```

### Trending Response
```json
{
  "content": [
    {
      "id": 123,
      "title": "Movie Title",
      "views_24h": 1500,
      "velocity": 1.25,
      "momentum": 0.15,
      "trending_score": 8.4
    }
  ]
}
```

</specifics>

<deferred>
## Deferred Ideas

- Real-time streaming analytics (requires WebSocket infrastructure)
- ML-powered engagement prediction (Phase 94)
- Per-segment analytics (requires video segmentation)
- A/B testing integration (future phase)

</deferred>

---

*Phase: 091-content-analytics-dashboard*
*Context gathered: 2026-04-30*
