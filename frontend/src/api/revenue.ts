import { fetchApi } from './auth';

export interface RevenueTrend {
  period: string;
  total_revenue: number;
  new_revenue: number;
  churned_revenue: number;
  net_revenue: number;
}

export interface SubscriptionMetrics {
  mrr: number;
  arr: number;
  growth_rate: number;
  churn_rate: number;
  active_subscribers: number;
  new_subscribers: number;
  churned_subscribers: number;
}

export async function getRevenueTrends(periodType = 'monthly', periods = 12) {
  return fetchApi<{ period_type: string; data: RevenueTrend[] }>(
    `/admin/analytics/revenue/trends?period_type=${periodType}&periods=${periods}`
  );
}

export async function getSubscriptionMetrics() {
  return fetchApi<SubscriptionMetrics>('/admin/analytics/revenue/metrics');
}

export async function getArpu() {
  return fetchApi<{ overall_arpu: number; arpu_by_plan: Record<string, number>; total_users: number; paying_users: number }>(
    '/admin/analytics/revenue/arpu'
  );
}

export async function getLtv() {
  return fetchApi<{ overall_ltv: number; ltv_by_plan: Record<string, number>; avg_subscription_months: number; total_lifetime_revenue: number }>(
    '/admin/analytics/revenue/ltv'
  );
}

export async function getPaymentFailures() {
  return fetchApi<{ total_failures: number; total_failed_amount: number; recovery_rate: number }>(
    '/admin/analytics/revenue/failures'
  );
}

export async function getRevenueForecast() {
  return fetchApi<{ current_mrr: number; projected_mrr_3m: number; projected_mrr_6m: number; projected_mrr_12m: number; growth_assumption: number }>(
    '/admin/analytics/revenue/forecast'
  );
}
