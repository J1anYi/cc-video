import api from './client';

export interface AudioTrack {
  id: number;
  language: string;
  title?: string;
  is_default: boolean;
  is_original: boolean;
  channel_layout: string;
  codec: string;
  bitrate: number;
}

export const audioTrackApi = {
  getVideoTracks: async (videoFileId: number) => {
    const response = await api.get('/audio-tracks/video/' + videoFileId);
    return response.data.tracks as AudioTrack[];
  },

  createTrack: async (data: {
    video_file_id: number;
    language: string;
    file_path: string;
    title?: string;
    is_default?: boolean;
    is_original?: boolean;
    channel_layout?: string;
  }) => {
    const response = await api.post('/audio-tracks', data);
    return response.data;
  },

  setDefaultTrack: async (trackId: number, videoFileId: number) => {
    const response = await api.put('/audio-tracks/' + trackId + '/default', null, {
      params: { video_file_id: videoFileId },
    });
    return response.data;
  },

  deleteTrack: async (trackId: number) => {
    const response = await api.delete('/audio-tracks/' + trackId);
    return response.data;
  },
};
