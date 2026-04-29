import api from './client';

export interface RecPrefs {
  genre_weights: Record<string, number>;
  recency_weight: number;
  social_weight: number;
  popularity_weight: number;
}

export const recInsightsApi = {
  getPrefs: async (): Promise<RecPrefs> => {
    const response = await api.get('/users/me/recommendation-preferences');
    return response.data;
  },
  updatePrefs: async (data: Partial<RecPrefs>): Promise<RecPrefs> => {
    const response = await api.patch('/users/me/recommendation-preferences', data);
    return response.data.preferences;
  }
};
