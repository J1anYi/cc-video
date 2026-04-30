import api from './client';

export interface PlaybackSettings {
  default_speed: number;
  auto_skip_intro: boolean;
  auto_skip_credits: boolean;
  auto_next_episode: boolean;
  pip_enabled: boolean;
  keyboard_shortcuts?: Record<string, string>;
}

export interface WatchProgress {
  movie_id: number;
  position_seconds: number;
  duration_seconds: number;
  completion_percentage: number;
}

export const playbackApi = {
  getSettings: async () => {
    const response = await api.get('/playback/settings');
    return response.data as PlaybackSettings;
  },

  updateSettings: async (data: Partial<PlaybackSettings>) => {
    const response = await api.put('/playback/settings', data);
    return response.data;
  },

  saveProgress: async (data: { movie_id: number; position_seconds: number; duration_seconds: number }) => {
    const response = await api.post('/playback/progress', data);
    return response.data;
  },

  getProgress: async (movieId: number) => {
    const response = await api.get('/playback/progress/' + movieId);
    return response.data as WatchProgress;
  },

  getAllProgress: async () => {
    const response = await api.get('/playback/progress');
    return response.data.progress as WatchProgress[];
  },
};
