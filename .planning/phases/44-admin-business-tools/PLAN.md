# PLAN: Phase 44 - Admin Business Tools

**Milestone:** v2.2 Monetization & Business
**Phase:** 44
**Goal:** Implement admin tools for business management

## Requirements

- ADMIN-01: Revenue dashboard
- ADMIN-02: Subscription analytics
- ADMIN-03: Churn tracking and reporting
- ADMIN-04: Promotional code management
- ADMIN-05: Customer support tools

## Success Criteria

1. Revenue metrics displayed accurately
2. Subscription analytics available
3. Churn reports generated
4. Promo codes managed through admin
5. Customer support can view subscriptions

## Implementation Plan

### Task 1: Backend - Revenue Dashboard API
- Calculate MRR and ARR
- Track revenue by tier
- Calculate average revenue per user
- Show revenue trends

### Task 2: Backend - Subscription Analytics
- Track subscription counts by tier
- Calculate conversion rates
- Monitor subscription changes
- Export subscription data

### Task 3: Backend - Churn Analysis
- Track cancellation reasons
- Calculate churn rate
- Identify at-risk customers
- Generate churn reports

### Task 4: Backend - Promo Code System
- Create PromoCode model
- Implement code validation
- Track code usage
- Support discount types

### Task 5: Backend - Customer Support Tools
- Admin subscription lookup
- Manual subscription adjustments
- Impersonation for support
- Support ticket reference

### Task 6: Frontend - Revenue Dashboard
- Create revenue overview page
- Show MRR/ARR charts
- Display revenue breakdown
- Show growth metrics

### Task 7: Frontend - Promo Code Management
- Create promo code list page
- Add promo code creation form
- Edit promo code details
- Show usage statistics

## Dependencies

- Subscription system (Phase 41)
- Payment integration (Phase 42)
- Admin dashboard (Phase 28)

## Risks

- Data accuracy for financial reports
- Mitigation: Reconcile with Stripe data

---
*Phase plan created: 2026-04-30*
