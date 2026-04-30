# Phase 93: Revenue Analytics - Context

**Gathered:** 2026-04-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement comprehensive revenue analytics for subscription-based video streaming.

**Delivers:**
- Revenue trend analysis (daily, weekly, monthly)
- Subscription metrics dashboard (MRR, churn, growth)
- Revenue per user analysis (ARPU, LTV)
- Payment failure analysis
- Revenue forecasting (simple projection)

</domain>

<decisions>
## Implementation Decisions

### Data Model
- **Subscription** model: Track subscription status, plan, billing
- **PaymentTransaction** model: Record all payment attempts
- **RevenueAnalytics** model: Cached revenue metrics
- **RevenuePerUser** model: ARPU and LTV calculations

### API Endpoints
- GET /admin/analytics/revenue/trends
- GET /admin/analytics/revenue/metrics
- GET /admin/analytics/revenue/arpu
- GET /admin/analytics/revenue/ltv
- GET /admin/analytics/revenue/failures
- GET /admin/analytics/revenue/forecast

### Revenue Metrics
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- ARPU (Average Revenue Per User)
- LTV (Lifetime Value)
- Churn Rate
- Growth Rate

</decisions>

<specifics>
### Subscription Model
- user_id, plan, status, started_at, expires_at, monthly_price

### Payment Transaction
- user_id, amount, currency, status, failure_reason, processed_at

### Revenue Analytics
- period, total_revenue, new_revenue, churned_revenue, net_revenue

</specifics>

<deferred>
- ML-based revenue forecasting (Phase 94)
- Real-time payment webhooks
- Multiple currency support
</deferred>

---

*Phase: 093-revenue-analytics*
*Context gathered: 2026-04-30*
