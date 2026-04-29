import api from './client';

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

export const analyticsApi = {
  getAnalytics: async (refresh = false): Promise<AnalyticsData> => {
    const response = await api.get('/users/me/analytics', {
      params: { refresh }
    });
    return response.data;
  },

  getWatchTime: async (): Promise<WatchTimeStats> => {
    const response = await api.get('/users/me/analytics/watch-time');
    return response.data;
  },

  getGenreBreakdown: async (): Promise<Record<string, number>> => {
    const response = await api.get('/users/me/analytics/genres');
    return response.data;
  },

  getTimePatterns: async (): Promise<{
    hourly: Record<string, number>;
    daily: Record<string, number>;
  }> => {
    const response = await api.get('/users/me/analytics/patterns');
    return response.data;
  },

  getActivityTimeline: async (params?: {
    activity_type?: string;
    skip?: number;
    limit?: number;
  }): Promise<{ activities: ActivityItem[]; total: number }> => {
    const response = await api.get('/users/me/analytics/timeline', { params });
    return response.data;
  },

  exportData: async (format: 'json' | 'csv' = 'json'): Promise<Blob> => {
    const response = await api.get('/users/me/analytics/export', {
      params: { format },
      responseType: 'blob'
    });
    return response.data;
  }
};
