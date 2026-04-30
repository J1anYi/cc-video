---
wave: 1
depends_on: []
files_modified:
  - backend/app/models/user_journey.py
  - backend/app/services/user_behavior_service.py
  - backend/app/routes/user_behavior.py
  - backend/app/schemas/user_behavior.py
  - backend/app/main.py
  - frontend/src/api/userBehavior.ts
  - frontend/src/routes/admin/UserBehavior.tsx
  - frontend/src/components/analytics/CohortTable.tsx
  - frontend/src/components/analytics/ChurnRiskList.tsx
requirements_addressed:
  - UBA-01
  - UBA-02
  - UBA-03
  - UBA-04
  - UBA-05
autonomous: true
---

# Plan: User Behavior Analytics Implementation

**Objective:** Implement comprehensive user behavior analytics for understanding journeys, sessions, segments, cohorts, and churn.

## Task 1: Create UserJourney Model

<read_first>
- backend/app/models/user_analytics.py
- backend/app/models/user.py
- backend/app/database.py
</read_first>

<action>
Create `backend/app/models/user_journey.py` with:

1. **UserJourneyEvent model**:
   - id: Integer, primary key
   - user_id: Integer, ForeignKey to users.id
   - session_id: String(100) - session identifier
   - event_type: String(50) - page_view, action, play, pause, search
   - event_data: JSON - event-specific data
   - page_url: String(500) - current page
   - referrer_url: String(500) - previous page (nullable)
   - created_at: DateTime

2. **UserSessionAnalytics model**:
   - id: Integer, primary key
   - user_id: Integer, ForeignKey to users.id
   - session_count: Integer, default 0
   - avg_session_duration_seconds: Integer, default 0
   - bounce_rate: Float, default 0.0
   - peak_hour: Integer, default 0
   - last_session_at: DateTime (nullable)

3. **UserSegment model**:
   - id: Integer, primary key
   - name: String(100)
   - description: String(500) (nullable)
   - rules: JSON - segment definition
   - member_count: Integer, default 0
   - created_at: DateTime
   - updated_at: DateTime

4. **CohortAnalytics model**:
   - id: Integer, primary key
   - cohort_key: String(20)
   - signup_count: Integer
   - d1_retention: Float (nullable)
   - d7_retention: Float (nullable)
   - d14_retention: Float (nullable)
   - d30_retention: Float (nullable)
   - created_at: DateTime

5. **ChurnRisk model**:
   - id: Integer, primary key
   - user_id: Integer, ForeignKey to users.id, unique
   - risk_score: Float (0-100)
   - risk_factors: JSON
   - last_calculated: DateTime
</action>

<acceptance_criteria>
- File backend/app/models/user_journey.py exists
- Contains all 5 models with specified fields
- Models use SQLAlchemy 2.0 Mapped types
</acceptance_criteria>

---

## Task 2: Create User Behavior Schemas

<read_first>
- backend/app/schemas/content_analytics.py
- backend/app/models/user_journey.py
</read_first>

<action>
Create `backend/app/schemas/user_behavior.py` with all Pydantic models for request/response handling.
</action>

<acceptance_criteria>
- File backend/app/schemas/user_behavior.py exists
- Contains JourneyEventResponse, UserJourneyResponse, SessionMetricsResponse, SegmentRule, SegmentResponse, CreateSegmentRequest, CohortResponse, ChurnRiskUserResponse
</acceptance_criteria>

---

## Task 3: Create User Behavior Service

<read_first>
- backend/app/services/content_analytics_service.py
- backend/app/models/user_journey.py
</read_first>

<action>
Create `backend/app/services/user_behavior_service.py` with UserBehaviorService class implementing:
- track_event(), get_user_journey(), compute_session_metrics()
- create_segment(), get_segments(), evaluate_user_for_segment()
- get_cohort_analytics(), calculate_all_cohorts()
- calculate_churn_risk(), get_at_risk_users(), update_all_churn_risks()
</action>

<acceptance_criteria>
- File backend/app/services/user_behavior_service.py exists
- Contains UserBehaviorService class with all methods
</acceptance_criteria>

---

## Task 4: Create User Behavior Routes

<read_first>
- backend/app/routes/content_analytics.py
- backend/app/dependencies.py
</read_first>

<action>
Create `backend/app/routes/user_behavior.py` with 7 endpoints:
- POST /admin/analytics/journeys/track
- GET /admin/analytics/journeys/{user_id}
- GET /admin/analytics/sessions
- GET /admin/analytics/segments
- POST /admin/analytics/segments
- GET /admin/analytics/cohorts
- GET /admin/analytics/churn
</action>

<acceptance_criteria>
- File backend/app/routes/user_behavior.py exists
- All 7 endpoints implemented with require_admin
</acceptance_criteria>

---

## Task 5: Register Routes in Main

<read_first>
- backend/app/main.py
</read_first>

<action>
Add user_behavior_router import and include_router to main.py
</action>

<acceptance_criteria>
- main.py updated with user_behavior_router
</acceptance_criteria>

---

## Task 6: Create Frontend API Client

<read_first>
- frontend/src/api/contentAnalytics.ts
</read_first>

<action>
Create `frontend/src/api/userBehavior.ts` with TypeScript interfaces and API functions.
</action>

<acceptance_criteria>
- File frontend/src/api/userBehavior.ts exists
</acceptance_criteria>

---

## Task 7: Create User Behavior Dashboard

<read_first>
- frontend/src/routes/admin/ContentAnalytics.tsx
</read_first>

<action>
Create `frontend/src/routes/admin/UserBehavior.tsx` with tab-based layout for Journeys, Sessions, Cohorts, Churn.
</action>

<acceptance_criteria>
- File frontend/src/routes/admin/UserBehavior.tsx exists
</acceptance_criteria>

---

## Task 8: Create Cohort Table Component

<action>
Create `frontend/src/components/analytics/CohortTable.tsx` for retention heatmap.
</action>

<acceptance_criteria>
- File frontend/src/components/analytics/CohortTable.tsx exists
</acceptance_criteria>

---

## Task 9: Create Churn Risk List Component

<action>
Create `frontend/src/components/analytics/ChurnRiskList.tsx` for at-risk users.
</action>

<acceptance_criteria>
- File frontend/src/components/analytics/ChurnRiskList.tsx exists
</acceptance_criteria>

---

## Task 10: Integration Testing

<action>
Test all endpoints and frontend rendering.
</action>

<acceptance_criteria>
- All tests pass
</acceptance_criteria>

---

## Verification Criteria

1. UBA-01 Journey tracking: Events tracked and retrievable
2. UBA-02 Session analysis: Metrics calculated from sessions
3. UBA-03 Segmentation: Segments created with rules
4. UBA-04 Cohort analysis: Retention by signup cohort
5. UBA-05 Churn prediction: Risk scores calculated
