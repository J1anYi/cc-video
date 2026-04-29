import { fetchApi } from './auth';

export interface WatchTimeStats {
  total_hours: number;
  total_movies: number;
}

export interface AnalyticsData {
  watch_time: WatchTimeStats;
  genre_breakdown: Record<string, number>;
  hourly_pattern: Record<string, number>;
  daily_pattern: Record<string, number>;
  last_updated: string | null;
}

export interface ActivityItem {
  id: number;
  type: string;
  movie_id: number | null;
  created_at: string;
}

export async function getAnalytics(refresh = false): Promise<AnalyticsData> {
  return fetchApi<AnalyticsData>(`/users/me/analytics?refresh=${refresh}`);
}

export async function getWatchTime(): Promise<WatchTimeStats> {
  return fetchApi<WatchTimeStats>('/users/me/analytics/watch-time');
}

export async function getGenreBreakdown(): Promise<Record<string, number>> {
  return fetchApi<Record<string, number>>('/users/me/analytics/genres');
}

export async function getTimePatterns(): Promise<{
  hourly: Record<string, number>;
  daily: Record<string, number>;
}> {
  return fetchApi<{
    hourly: Record<string, number>;
    daily: Record<string, number>;
  }>('/users/me/analytics/patterns');
}

export async function getActivityTimeline(params?: {
  activity_type?: string;
  skip?: number;
  limit?: number;
}): Promise<{ activities: ActivityItem[]; total: number }> {
  const query = new URLSearchParams();
  if (params?.activity_type) query.set('activity_type', params.activity_type);
  if (params?.skip) query.set('skip', params.skip.toString());
  if (params?.limit) query.set('limit', params.limit.toString());
  return fetchApi<{ activities: ActivityItem[]; total: number }>(
    `/users/me/analytics/timeline?${query.toString()}`
  );
}

export async function exportData(format: 'json' | 'csv' = 'json'): Promise<Blob> {
  const token = localStorage.getItem('token');
  const response = await fetch(`/api/v1/users/me/analytics/export?format=${format}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.blob();
}
