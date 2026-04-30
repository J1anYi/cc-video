import { fetchApi } from './auth';

export interface JourneyEvent {
  id: number;
  user_id: number;
  event_type: string;
  event_data: Record<string, unknown> | null;
  page_url: string;
  referrer_url: string | null;
  created_at: string;
}

export interface UserJourney {
  user_id: number;
  events: JourneyEvent[];
  total_events: number;
}

export interface SessionMetrics {
  total_sessions: number;
  avg_duration_seconds: number;
  bounce_rate: number;
  peak_hour: number;
}

export interface SegmentRule {
  field: string;
  op: string;
  value: unknown;
}

export interface Segment {
  id: number;
  name: string;
  description: string | null;
  rules: SegmentRule[];
  member_count: number;
  created_at: string;
}

export interface CreateSegmentRequest {
  name: string;
  description?: string;
  rules: SegmentRule[];
}

export interface Cohort {
  cohort_key: string;
  signup_count: number;
  d1_retention: number | null;
  d7_retention: number | null;
  d14_retention: number | null;
  d30_retention: number | null;
}

export interface ChurnRiskUser {
  user_id: number;
  email: string;
  risk_score: number;
  risk_factors: Record<string, unknown> | null;
  last_login_days: number | null;
}

export async function trackJourneyEvent(data: {
  user_id: number;
  session_id: string;
  event_type: string;
  event_data?: Record<string, unknown>;
  page_url?: string;
  referrer_url?: string;
}): Promise<{ success: boolean; event_id: number }> {
  return fetchApi('/admin/analytics/journey/track', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function getUserJourney(userId: number, limit = 100): Promise<UserJourney> {
  return fetchApi<UserJourney>(`/admin/analytics/journeys/${userId}?limit=${limit}`);
}

export async function getSessionMetrics(userId?: number): Promise<SessionMetrics> {
  const query = userId ? `?user_id=${userId}` : '';
  return fetchApi<SessionMetrics>(`/admin/analytics/sessions${query}`);
}

export async function getSegments(): Promise<Segment[]> {
  return fetchApi<Segment[]>('/admin/analytics/segments');
}

export async function createSegment(data: CreateSegmentRequest): Promise<Segment> {
  return fetchApi<Segment>('/admin/analytics/segments', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function getCohortAnalytics(weeks = 12): Promise<Cohort[]> {
  return fetchApi<Cohort[]>(`/admin/analytics/cohorts?weeks=${weeks}`);
}

export async function getChurnRiskUsers(threshold = 50, limit = 100): Promise<ChurnRiskUser[]> {
  return fetchApi<ChurnRiskUser[]>(`/admin/analytics/churn?threshold=${threshold}&limit=${limit}`);
}
