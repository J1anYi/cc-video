---
wave: 1
depends_on: []
files_modified:
  - backend/app/models/content_analytics.py
  - backend/app/services/content_analytics_service.py
  - backend/app/routes/content_analytics.py
  - backend/app/schemas/content_analytics.py
  - backend/app/main.py
  - frontend/src/api/contentAnalytics.ts
  - frontend/src/routes/admin/ContentAnalytics.tsx
  - frontend/src/components/analytics/EngagementHeatmap.tsx
  - frontend/src/components/analytics/CompletionChart.tsx
requirements_addressed:
  - CA-01
  - CA-02
  - CA-03
  - CA-04
  - CA-05
autonomous: true
---

# Plan: Content Analytics Dashboard Implementation

**Objective:** Implement comprehensive content performance analytics for administrators.

## Task 1: Create ContentAnalytics Model

<read_first>
- backend/app/models/user_analytics.py
- backend/app/models/movie.py
- backend/app/database.py
</read_first>

<action>
Create `backend/app/models/content_analytics.py` with:

1. **ContentAnalytics model**:
   - `id`: Integer, primary key
   - `content_id`: Integer, ForeignKey to movies.id
   - `content_type`: String (movie, series, episode)
   - `total_views`: Integer, default 0
   - `unique_viewers`: Integer, default 0
   - `total_watch_time_seconds`: Integer, default 0
   - `avg_completion_pct`: Float, default 0.0
   - `engagement_score`: Float, default 0.0
   - `last_24h_views`: Integer, default 0
   - `previous_24h_views`: Integer, default 0
   - `velocity`: Float, default 1.0
   - `momentum`: Float, default 0.0
   - `trending_score`: Float, default 0.0
   - `last_updated`: DateTime

2. **ContentEngagementHeatmap model**:
   - `id`: Integer, primary key
   - `content_id`: Integer, ForeignKey to movies.id
   - `timestamp_seconds`: Integer
   - `engagement_pct`: Float
   - `play_count`: Integer, default 0
   - `pause_count`: Integer, default 0
   - `seek_count`: Integer, default 0
   - `rewind_count`: Integer, default 0
   - `drop_count`: Integer, default 0

3. Add relationship in Movie model to ContentAnalytics (one-to-one)
</action>

<acceptance_criteria>
- File `backend/app/models/content_analytics.py` exists
- Contains ContentAnalytics class with all specified fields
- Contains ContentEngagementHeatmap class with all specified fields
- Models inherit from Base and use SQLAlchemy 2.0 Mapped types
</acceptance_criteria>

---

## Task 2: Create Content Analytics Schemas

<read_first>
- backend/app/schemas/analytics.py
- backend/app/models/content_analytics.py
</read_first>

<action>
Create `backend/app/schemas/content_analytics.py` with:

1. **ContentMetricsResponse**:
   - content_id: int
   - title: str
   - total_views: int
   - unique_viewers: int
   - avg_completion_pct: float
   - total_watch_time_hours: float
   - engagement_score: float

2. **HeatmapDataPoint**:
   - timestamp_seconds: int
   - engagement_pct: float
   - play_count: int
   - pause_count: int
   - seek_count: int
   - rewind_count: int

3. **HeatmapResponse**:
   - content_id: int
   - duration_seconds: int
   - samples: list[HeatmapDataPoint]

4. **CompletionAnalysisResponse**:
   - content_id: int
   - completion_rate: float
   - avg_watch_duration_seconds: int
   - drop_off_points: list[dict] (timestamp, drop_pct)

5. **ContentComparisonItem**:
   - content_id: int
   - title: str
   - metrics: ContentMetricsResponse

6. **TrendingContentItem**:
   - id: int
   - title: str
   - views_24h: int
   - velocity: float
   - momentum: float
   - trending_score: float
</action>

<acceptance_criteria>
- File `backend/app/schemas/content_analytics.py` exists
- Contains all 6 Pydantic models with specified fields
- All models inherit from BaseModel
</acceptance_criteria>

---

## Task 3: Create Content Analytics Service

<read_first>
- backend/app/services/analytics.py
- backend/app/models/content_analytics.py
- backend/app/models/viewing_session.py
- backend/app/models/watch_history.py
</read_first>

<action>
Create `backend/app/services/content_analytics_service.py` with ContentAnalyticsService class:

1. **get_content_metrics(content_id)**: Fetch cached metrics for a content item
2. **compute_content_metrics(content_id)**: Calculate metrics from viewing_sessions
3. **get_engagement_heatmap(content_id)**: Generate heatmap data
4. **compute_completion_analysis(content_id)**: Analyze completion patterns
5. **compare_content(content_ids)**: Compare metrics across content items
6. **get_trending_content(limit, time_range)**: Get trending content with velocity
7. **update_trending_scores()**: Background task to update velocity/momentum
8. **refresh_content_analytics(content_id)**: Refresh cached metrics

Use existing patterns from analytics.py for caching strategy (hourly refresh).
</action>

<acceptance_criteria>
- File `backend/app/services/content_analytics_service.py` exists
- Contains ContentAnalyticsService class with all 8 methods
- Uses SQLAlchemy async patterns matching existing analytics.py
- content_analytics_service singleton instance created
</acceptance_criteria>

---

## Task 4: Create Content Analytics Routes

<read_first>
- backend/app/routes/analytics.py
- backend/app/dependencies.py
- backend/app/services/content_analytics_service.py
</read_first>

<action>
Create `backend/app/routes/content_analytics.py` with:

1. `GET /admin/content/analytics/trending` - Get trending content list
   - Query params: limit, time_range
   - Returns: list[TrendingContentItem]
   - Requires: require_admin dependency

2. `GET /admin/content/{content_id}/analytics` - Get content metrics
   - Path param: content_id
   - Query params: refresh (optional)
   - Returns: ContentMetricsResponse
   - Requires: require_admin dependency

3. `GET /admin/content/{content_id}/heatmap` - Get engagement heatmap
   - Path param: content_id
   - Returns: HeatmapResponse
   - Requires: require_admin dependency

4. `GET /admin/content/{content_id}/completion` - Get completion analysis
   - Path param: content_id
   - Returns: CompletionAnalysisResponse
   - Requires: require_admin dependency

5. `POST /admin/content/compare` - Compare content items
   - Body: {"content_ids": [1, 2, 3]}
   - Returns: list[ContentComparisonItem]
   - Requires: require_admin dependency

All routes use require_admin dependency for access control.
</action>

<acceptance_criteria>
- File `backend/app/routes/content_analytics.py` exists
- Contains router with prefix "/admin/content" and tag "content-analytics"
- All 5 endpoints implemented with correct signatures
- All endpoints use require_admin dependency
- Router exported as `router`
</acceptance_criteria>

---

## Task 5: Register Routes in Main

<read_first>
- backend/app/main.py
- backend/app/routes/content_analytics.py
</read_first>

<action>
Update `backend/app/main.py`:

1. Add import: `from app.routes.content_analytics import router as content_analytics_router`
2. Add router include: `app.include_router(content_analytics_router)` after other admin routers

Insert the import at line ~45 with other route imports.
Insert the include_router at line ~117 after ai_editing_router.
</action>

<acceptance_criteria>
- `backend/app/main.py` contains import for content_analytics_router
- `backend/app/main.py` contains app.include_router(content_analytics_router)
- Import is grouped with other route imports
</acceptance_criteria>

---

## Task 6: Create Frontend API Client

<read_first>
- frontend/src/api/analytics.ts
- frontend/src/api/types.ts
</read_first>

<action>
Create `frontend/src/api/contentAnalytics.ts` with:

1. **TypeScript interfaces** matching backend schemas:
   - ContentMetrics
   - HeatmapDataPoint
   - HeatmapData
   - CompletionAnalysis
   - TrendingContent

2. **API functions**:
   - `getTrendingContent(limit?, timeRange?)`: GET /admin/content/analytics/trending
   - `getContentMetrics(contentId, refresh?)`: GET /admin/content/{id}/analytics
   - `getContentHeatmap(contentId)`: GET /admin/content/{id}/heatmap
   - `getCompletionAnalysis(contentId)`: GET /admin/content/{id}/completion
   - `compareContent(contentIds)`: POST /admin/content/compare

Use fetchApi helper from auth.ts for authenticated requests.
</action>

<acceptance_criteria>
- File `frontend/src/api/contentAnalytics.ts` exists
- Contains all 5 TypeScript interfaces
- Contains all 5 API functions using fetchApi
- Exports all types and functions
</acceptance_criteria>

---

## Task 7: Create Content Analytics Dashboard Page

<read_first>
- frontend/src/routes/admin/AdminDashboard.tsx (if exists)
- frontend/src/api/contentAnalytics.ts
</read_first>

<action>
Create `frontend/src/routes/admin/ContentAnalytics.tsx`:

1. **Main dashboard component** with:
   - Top trending content list (top 10 with velocity indicators)
   - Content selector for detailed analytics
   - Metrics cards: total views, unique viewers, avg completion, engagement score
   - Engagement heatmap visualization
   - Completion curve chart
   - Content comparison tool

2. **State management**:
   - Use React hooks (useState, useEffect)
   - Loading states for async data
   - Error handling with error boundary

3. **Layout**:
   - Grid layout for metrics cards
   - Full-width heatmap section
   - Side-by-side comparison view

4. **Styling**:
   - Match existing admin dashboard styling
   - Use Tailwind CSS classes
</action>

<acceptance_criteria>
- File `frontend/src/routes/admin/ContentAnalytics.tsx` exists
- Component renders trending content list
- Component shows content metrics cards
- Component includes content selector
- Uses contentAnalytics API functions
- Handles loading and error states
</acceptance_criteria>

---

## Task 8: Create Engagement Heatmap Component

<read_first>
- frontend/src/routes/admin/ContentAnalytics.tsx
- frontend/src/api/contentAnalytics.ts
</read_first>

<action>
Create `frontend/src/components/analytics/EngagementHeatmap.tsx`:

1. **Canvas-based heatmap visualization**:
   - X-axis: video timeline (0 to duration)
   - Y-axis: engagement percentage (0-100%)
   - Color gradient: green (high) -> yellow -> red (low)
   - Hover tooltip showing timestamp and engagement

2. **Props**:
   - `heatmapData: HeatmapData`
   - `width: number` (default 800)
   - `height: number` (default 100)
   - `showTooltip: boolean` (default true)

3. **Interactivity**:
   - Mouse hover shows timestamp and engagement
   - Click-to-seek integration (optional, callback prop)

4. **Canvas drawing**:
   - Draw rectangle for each sample point
   - Color based on engagement percentage
   - Smooth transition between segments
</action>

<acceptance_criteria>
- File `frontend/src/components/analytics/EngagementHeatmap.tsx` exists
- Component renders canvas element
- Component draws colored segments based on engagement
- Hover tooltip displays timestamp and engagement value
- Component accepts heatmapData prop
</acceptance_criteria>

---

## Task 9: Create Completion Chart Component

<read_first>
- frontend/src/routes/admin/ContentAnalytics.tsx
- frontend/src/api/contentAnalytics.ts
</read_first>

<action>
Create `frontend/src/components/analytics/CompletionChart.tsx`:

1. **Line chart showing retention curve**:
   - X-axis: video timeline percentage (0-100%)
   - Y-axis: viewers remaining percentage (0-100%)
   - Shows drop-off points clearly

2. **Props**:
   - `completionData: CompletionAnalysis`
   - `width: number` (default 800)
   - `height: number` (default 300)

3. **Features**:
   - Mark significant drop-off points
   - Show average completion line
   - Hover shows exact percentage

4. **Implementation**:
   - Use simple SVG line chart (no external library)
   - Or use canvas for performance
</action>

<acceptance_criteria>
- File `frontend/src/components/analytics/CompletionChart.tsx` exists
- Component renders line chart
- Chart shows retention curve with drop-offs
- Component accepts completionData prop
</acceptance_criteria>

---

## Task 10: Integration Testing

<read_first>
- backend/app/routes/content_analytics.py
- frontend/src/api/contentAnalytics.ts
</read_first>

<action>
Test the complete content analytics flow:

1. **Backend API tests**:
   - Start backend server
   - Test GET /admin/content/analytics/trending returns 200
   - Test GET /admin/content/1/analytics returns metrics
   - Test GET /admin/content/1/heatmap returns heatmap data
   - Test GET /admin/content/1/completion returns analysis
   - Test POST /admin/content/compare with content IDs

2. **Frontend integration**:
   - Navigate to /admin/analytics
   - Verify trending content list loads
   - Select a content item and verify metrics display
   - Verify heatmap renders
   - Verify completion chart renders

3. **Database verification**:
   - Confirm ContentAnalytics table created
   - Confirm ContentEngagementHeatmap table created
</action>

<acceptance_criteria>
- Backend server starts without errors
- All 5 API endpoints return valid responses
- Frontend page renders without errors
- Trending content list displays
- Content metrics cards show data
- Heatmap component renders
- Completion chart component renders
</acceptance_criteria>

---

## Verification Criteria

1. **CA-01 Real-time metrics**: Content metrics endpoint returns views, unique viewers, completion rate
2. **CA-02 Engagement heatmaps**: Heatmap endpoint returns timestamped engagement data
3. **CA-03 Completion analysis**: Completion endpoint returns drop-off analysis
4. **CA-04 Content comparison**: Compare endpoint returns side-by-side metrics
5. **CA-05 Trending analysis**: Trending endpoint returns velocity/momentum scores

## Must-Haves

- ContentAnalytics and ContentEngagementHeatmap models created
- All 5 API endpoints functional
- Frontend dashboard renders with data
- Heatmap component visualizes engagement
- Completion chart shows retention curve
- Admin access control enforced on all endpoints
