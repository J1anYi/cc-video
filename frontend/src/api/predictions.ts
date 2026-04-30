import { fetchApi } from './auth';

export interface ContentSuccess {
  content_id: number;
  title: string;
  success_score: number;
  predicted_views: number;
  confidence: number;
  factors?: Record<string, unknown>;
}

export interface DemandPoint {
  date: string;
  predicted_views: number;
  predicted_hours: number;
  confidence: number;
}

export interface PricingSuggestion {
  plan: string;
  current_price: number;
  suggested_price: number;
  expected_revenue_change: number;
  reasoning?: string;
}

export interface ContentGap {
  genre: string;
  demand_score: number;
  supply_score: number;
  gap_score: number;
  recommendation?: string;
}

export async function predictContentSuccess(contentId: number) {
  return fetchApi<ContentSuccess>(`/admin/predictions/content/${contentId}/success`);
}

export async function getDemandForecast(days = 30) {
  return fetchApi<{ forecasts: DemandPoint[]; total_predicted_views: number }>(
    `/admin/predictions/demand?days=${days}`
  );
}

export async function predictLtv(userId: number) {
  return fetchApi<{ user_id: number; predicted_ltv: number; confidence: number }>(
    `/admin/predictions/ltv/${userId}`
  );
}

export async function getPricingSuggestions() {
  return fetchApi<{ suggestions: PricingSuggestion[] }>('/admin/predictions/pricing');
}

export async function getContentGaps() {
  return fetchApi<{ gaps: ContentGap[] }>('/admin/predictions/content-gaps');
}
