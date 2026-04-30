import api from './client';

export interface StreamVariant {
  id: number;
  quality: string;
  resolution: string;
  bitrate: number;
  hls_url: string;
  manifest_url?: string;
}

export interface BandwidthStats {
  avg_bandwidth_kbps: number;
  total_measurements: number;
  avg_buffer_events: number;
  avg_rebuffer_time_ms: number;
}

export interface QualityPreferences {
  preferred_quality: string;
  auto_adjust: boolean;
  limit_mobile_data: boolean;
}

export const streamingApi = {
  getMovieVariants: async (movieId: number) => {
    const response = await api.get('/streaming/movies/' + movieId + '/variants');
    return response.data.variants as StreamVariant[];
  },

  recordMetric: async (data: {
    bandwidth_kbps: number;
    quality_selected?: string;
    quality_played?: string;
    movie_id?: number;
    buffer_events?: number;
    rebuffer_time_ms?: number;
  }) => {
    const response = await api.post('/streaming/metrics', data);
    return response.data;
  },

  getBandwidthStats: async () => {
    const response = await api.get('/streaming/stats');
    return response.data as BandwidthStats;
  },

  getRecommendedQuality: async (bandwidthKbps: number) => {
    const response = await api.get('/streaming/recommend', {
      params: { bandwidth_kbps: bandwidthKbps },
    });
    return response.data.recommended_quality as string;
  },

  getPreferences: async () => {
    const response = await api.get('/streaming/preferences');
    return response.data as QualityPreferences;
  },

  updatePreferences: async (data: {
    preferred_quality: string;
    auto_adjust?: boolean;
    limit_mobile_data?: boolean;
  }) => {
    const response = await api.put('/streaming/preferences', data);
    return response.data;
  },
};
