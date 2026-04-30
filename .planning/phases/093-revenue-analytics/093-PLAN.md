---
wave: 1
depends_on: []
files_modified:
  - backend/app/models/subscription.py
  - backend/app/services/revenue_service.py
  - backend/app/routes/revenue.py
  - backend/app/schemas/revenue.py
  - backend/app/main.py
  - frontend/src/api/revenue.ts
  - frontend/src/routes/admin/RevenueAnalytics.tsx
requirements_addressed:
  - RA-01
  - RA-02
  - RA-03
  - RA-04
  - RA-05
autonomous: true
---

# Plan: Revenue Analytics Implementation

## Task 1: Create Subscription Models
Create `backend/app/models/subscription.py` with Subscription, PaymentTransaction, RevenueAnalytics, RevenuePerUser models.

## Task 2: Create Revenue Schemas
Create `backend/app/schemas/revenue.py` with Pydantic models for all responses.

## Task 3: Create Revenue Service
Create `backend/app/services/revenue_service.py` with RevenueService class:
- get_revenue_trends(), get_subscription_metrics(), get_arpu()
- get_ltv_analysis(), get_payment_failures(), get_revenue_forecast()

## Task 4: Create Revenue Routes
Create `backend/app/routes/revenue.py` with 6 endpoints:
- GET /admin/analytics/revenue/trends
- GET /admin/analytics/revenue/metrics
- GET /admin/analytics/revenue/arpu
- GET /admin/analytics/revenue/ltv
- GET /admin/analytics/revenue/failures
- GET /admin/analytics/revenue/forecast

## Task 5: Register Routes in Main
Add revenue_router to main.py.

## Task 6: Create Frontend API Client
Create `frontend/src/api/revenue.ts`.

## Task 7: Create Revenue Dashboard
Create `frontend/src/routes/admin/RevenueAnalytics.tsx` with metrics cards and charts.

## Task 8: Integration Testing
Test all endpoints and frontend rendering.

## Verification Criteria
1. RA-01: Revenue trends tracked
2. RA-02: Subscription metrics displayed
3. RA-03: ARPU calculated
4. RA-04: Payment failures analyzed
5. RA-05: Revenue forecasting working
