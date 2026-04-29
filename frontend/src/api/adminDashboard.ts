import api from './client';

export interface DashboardMetrics {
  total_users: number;
  new_users_today: number;
  total_movies: number;
  views_today: number;
  pending_reports: number;
}

export interface ActivityItem {
  id: number;
  type: string;
  user_id: number;
  movie_id: number | null;
  created_at: string;
}

export interface DailyGrowth {
  date: string;
  count: number;
}

export interface UserGrowth {
  daily: DailyGrowth[];
  growth_rate: number;
}

export interface ContentHealth {
  pending_reports: number;
  stale_content: number;
}

export interface DashboardData {
  metrics: DashboardMetrics;
  activity: ActivityItem[];
  growth: UserGrowth;
  health: ContentHealth;
}

export const adminDashboardApi = {
  getDashboard: async (): Promise<DashboardData> => {
    const response = await api.get('/admin/dashboard');
    return response.data;
  }
};
