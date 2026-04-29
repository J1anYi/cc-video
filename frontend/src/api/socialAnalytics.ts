import api from './client';

export interface SocialAnalytics {
  influence_score: number;
  followers: number;
  following: number;
  follower_growth: { date: string; count: number }[];
  review_stats: {
    total_views: number;
    total_helpful_votes: number;
    review_count: number;
    avg_engagement: number;
  };
  top_reviews: { review_id: number; movie_id: number; content: string; helpful_votes: number }[];
}

export const socialAnalyticsApi = {
  getAnalytics: async (): Promise<SocialAnalytics> => {
    const response = await api.get('/users/me/social-analytics');
    return response.data;
  },
  refresh: async (): Promise<SocialAnalytics> => {
    const response = await api.get('/users/me/social-analytics/refresh');
    return response.data;
  },
  compare: async (userId: number): Promise<{ you: any; friend: any }> => {
    const response = await api.get('/users/me/social-analytics/compare/' + userId);
    return response.data;
  }
};
