# Phase 92: User Behavior Analytics - Context

**Gathered:** 2026-04-30
**Status:** Ready for planning
**Source:** Requirements analysis + existing codebase research

<domain>
## Phase Boundary

Implement comprehensive user behavior analytics for understanding user journeys, session patterns, segmentation, cohorts, and churn prediction.

**Delivers:**
- User journey tracking (pages visited, actions taken, paths)
- Session analysis (duration, patterns, bounce rates)
- User segmentation (by behavior, demographics, engagement)
- Cohort analysis (retention over time by signup cohorts)
- Churn prediction (identify at-risk users)

**NOT in scope:**
- Content analytics (Phase 91 complete)
- Revenue analytics (Phase 93)
- Predictive ML models (Phase 94 - this is simpler rule-based churn prediction)

</domain>

<decisions>
## Implementation Decisions

### Data Model
- **UserJourney model**: Track user navigation paths and actions
- **UserSessionAnalytics model**: Aggregate session metrics per user
- **UserSegment model**: Define and store segment membership
- **Cohort model**: Track cohorts by signup date
- **ChurnRisk model**: Store churn prediction scores

### API Endpoints
- `GET /admin/analytics/journeys` - List user journeys with filters
- `GET /admin/analytics/sessions` - Session analysis metrics
- `GET /admin/analytics/segments` - List user segments
- `POST /admin/analytics/segments` - Create segment
- `GET /admin/analytics/cohorts` - Cohort retention analysis
- `GET /admin/analytics/churn` - Churn risk users

### Journey Tracking
- Track page views via middleware or frontend events
- Store as lightweight events (user_id, action, timestamp, metadata)
- Aggregate for path analysis

### Session Analysis
- Use existing ViewingSession model for session duration
- Calculate bounce rate (single-page sessions)
- Pattern detection (peak hours, device usage)

### Segmentation
- Rule-based segments (e.g., "power users" = 10+ hours watch time)
- Segments recalculated daily
- Support custom segment definitions

### Cohort Analysis
- Group users by signup week/month
- Track retention at D1, D7, D14, D30
- Calculate cohort-specific metrics

### Churn Prediction
- Simple rule-based scoring (no ML in this phase)
- Factors: days since last login, declining watch time, low engagement
- Score 0-100, flag users above threshold

### Frontend Components
- UserJourneyView: Visualize user paths
- SessionMetricsDashboard: Session stats and charts
- SegmentManager: Create/manage segments
- CohortTable: Retention heatmap by cohort
- ChurnRiskList: At-risk users with risk scores

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Analytics Infrastructure
- `backend/app/models/user_analytics.py` — UserAnalytics model (already exists)
- `backend/app/services/analytics.py` — AnalyticsService patterns
- `backend/app/models/viewing_session.py` — ViewingSession model
- `backend/app/models/user.py` — User model with signup date

### Phase 91 (Just Completed)
- `backend/app/models/content_analytics.py` — Similar model patterns
- `backend/app/services/content_analytics_service.py` — Service patterns
- `backend/app/routes/content_analytics.py` — Route patterns

</canonical_refs>

<specifics>
## Specific Ideas

### Journey Event Structure
```json
{
  "user_id": 123,
  "event_type": "page_view" | "action" | "search" | "play" | "pause",
  "event_data": {"page": "/movies/123", "action": "play"},
  "session_id": "abc123",
  "timestamp": "2026-04-30T10:00:00Z"
}
```

### Segment Definition
```json
{
  "name": "Power Users",
  "rules": [
    {"field": "total_watch_time_hours", "op": ">=", "value": 10},
    {"field": "sessions_count", "op": ">=", "value": 5}
  ],
  "member_count": 1234
}
```

### Cohort Retention Response
```json
{
  "cohort": "2026-W17",
  "signup_count": 500,
  "retention": {
    "D1": 85,
    "D7": 60,
    "D14": 45,
    "D30": 30
  }
}
```

### Churn Risk Score
```python
# Simple scoring (not ML)
score = 0
if days_since_last_login > 7: score += 30
if days_since_last_login > 14: score += 20
if watch_time_this_week < watch_time_last_week * 0.5: score += 25
if total_sessions < 3: score += 15
# Threshold: score >= 50 = at-risk
```

</specifics>

<deferred>
## Deferred Ideas

- ML-based churn prediction (Phase 94)
- Real-time journey streaming (requires WebSocket)
- Advanced segmentation with ML clustering
- A/B testing integration
- Funnel analysis

</deferred>

---

*Phase: 092-user-behavior-analytics*
*Context gathered: 2026-04-30*
