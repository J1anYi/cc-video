import { fetchApi } from './auth';

export interface PlatformOverview {
  total_views: number;
  active_users: number;
  total_users: number;
  total_movies: number;
  total_watch_time_hours: number;
  engagement_rate: number;
}

export interface MovieMetrics {
  movie_id: number;
  total_views: number;
  unique_viewers: number;
  total_watch_time_hours: number;
  completion_rate: number;
  avg_rating: number | null;
  rating_count: number;
  review_count: number;
  engagement_score: number;
}

export interface TrendingItem {
  id: number;
  title: string;
  views: number;
  genre: string;
}

export interface RankingItem {
  id: number;
  title: string;
  genre: string;
  views: number;
  avg_rating: number | null;
  release_year: number | null;
}

export interface RetentionMetrics {
  new_users_30d: number;
  returning_users_7d: number;
  retention_rate: number;
}

export async function getOverview(): Promise<PlatformOverview> {
  return fetchApi<PlatformOverview>('/admin/metrics/overview');
}

export async function getMovieMetrics(movieId: number): Promise<MovieMetrics> {
  return fetchApi<MovieMetrics>(`/admin/metrics/movies/${movieId}`);
}

export async function getTrending(period = 'week', limit = 10): Promise<TrendingItem[]> {
  return fetchApi<TrendingItem[]>(`/admin/metrics/trending?period=${period}&limit=${limit}`);
}

export async function getRetention(): Promise<RetentionMetrics> {
  return fetchApi<RetentionMetrics>('/admin/metrics/retention');
}

export async function getRankings(params?: {
  sort_by?: string;
  genre?: string;
  limit?: number;
}): Promise<RankingItem[]> {
  const query = new URLSearchParams();
  if (params?.sort_by) query.set('sort_by', params.sort_by);
  if (params?.genre) query.set('genre', params.genre);
  if (params?.limit) query.set('limit', params.limit.toString());
  return fetchApi<RankingItem[]>(`/admin/metrics/rankings?${query.toString()}`);
}
