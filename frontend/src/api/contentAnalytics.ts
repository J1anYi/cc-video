import { fetchApi } from './auth';

export interface ContentMetrics {
  content_id: number;
  title: string;
  total_views: number;
  unique_viewers: number;
  avg_completion_pct: number;
  total_watch_time_hours: number;
  engagement_score: number;
  last_updated: string | null;
}

export interface HeatmapDataPoint {
  timestamp_seconds: number;
  engagement_pct: number;
  play_count: number;
  pause_count: number;
  seek_count: number;
  rewind_count: number;
}

export interface HeatmapData {
  content_id: number;
  duration_seconds: number;
  samples: HeatmapDataPoint[];
}

export interface DropOffPoint {
  timestamp_seconds: number;
  drop_pct: number;
}

export interface CompletionAnalysis {
  content_id: number;
  completion_rate: number;
  avg_watch_duration_seconds: number;
  drop_off_points: DropOffPoint[];
}

export interface TrendingContent {
  id: number;
  title: string;
  views_24h: number;
  velocity: number;
  momentum: number;
  trending_score: number;
  poster_url: string | null;
}

export interface TrendingContentResponse {
  content: TrendingContent[];
  time_range: string;
  generated_at: string;
}

export interface ContentComparisonItem {
  content_id: number;
  title: string;
  total_views: number;
  unique_viewers: number;
  avg_completion_pct: number;
  engagement_score: number;
}

export async function getTrendingContent(
  limit = 20,
  timeRange = '24h'
): Promise<TrendingContentResponse> {
  return fetchApi<TrendingContentResponse>(
    `/admin/content/analytics/trending?limit=${limit}&time_range=${timeRange}`
  );
}

export async function getContentMetrics(
  contentId: number,
  refresh = false
): Promise<ContentMetrics> {
  return fetchApi<ContentMetrics>(
    `/admin/content/${contentId}/analytics?refresh=${refresh}`
  );
}

export async function getContentHeatmap(contentId: number): Promise<HeatmapData> {
  return fetchApi<HeatmapData>(`/admin/content/${contentId}/heatmap`);
}

export async function getCompletionAnalysis(contentId: number): Promise<CompletionAnalysis> {
  return fetchApi<CompletionAnalysis>(`/admin/content/${contentId}/completion`);
}

export async function compareContent(contentIds: number[]): Promise<{ items: ContentComparisonItem[] }> {
  return fetchApi<{ items: ContentComparisonItem[] }>('/admin/content/compare', {
    method: 'POST',
    body: JSON.stringify({ content_ids: contentIds }),
  });
}
