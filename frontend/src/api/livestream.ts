import api from './client';

export interface LiveStream {
  id: number;
  title: string;
  description?: string;
  status: string;
  viewer_count: number;
  peak_viewers: number;
  started_at?: string;
  ended_at?: string;
}

export interface ScheduledStream {
  id: number;
  title: string;
  description?: string;
  scheduled_start: string;
  scheduled_end?: string;
  streamer_id: number;
}

export interface DVRSegment {
  id: number;
  segment_url: string;
  segment_duration: number;
  start_time: string;
  end_time: string;
}

export const livestreamApi = {
  createStream: async (title: string, description?: string) => {
    const response = await api.post('/live/streams', { title, description });
    return response.data;
  },

  getStreams: async () => {
    const response = await api.get('/live/streams');
    return response.data.streams as LiveStream[];
  },

  getStream: async (streamId: number) => {
    const response = await api.get('/live/streams/' + streamId);
    return response.data as LiveStream;
  },

  startStream: async (streamId: number) => {
    const response = await api.post('/live/streams/' + streamId + '/start');
    return response.data;
  },

  endStream: async (streamId: number) => {
    const response = await api.post('/live/streams/' + streamId + '/end');
    return response.data;
  },

  sendChat: async (streamId: number, message: string) => {
    const response = await api.post('/live/streams/' + streamId + '/chat', { message });
    return response.data;
  },

  sendReaction: async (streamId: number, reactionType: string) => {
    const response = await api.post('/live/streams/' + streamId + '/reactions', { reaction_type: reactionType });
    return response.data;
  },

  scheduleStream: async (data: {
    title: string;
    scheduled_start: string;
    description?: string;
    scheduled_end?: string;
    is_recurring?: boolean;
    recurrence_pattern?: string;
  }) => {
    const response = await api.post('/live/schedule', data);
    return response.data;
  },

  getUpcomingStreams: async (limit = 20) => {
    const response = await api.get('/live/upcoming', { params: { limit } });
    return response.data.schedules as ScheduledStream[];
  },

  getDVRSegments: async (streamId: number) => {
    const response = await api.get('/live/streams/' + streamId + '/dvr');
    return response.data.segments as DVRSegment[];
  },

  subscribeToStream: async (streamId: number, notificationType = 'start', notifyBeforeMinutes = 5) => {
    const response = await api.post('/live/streams/' + streamId + '/subscribe', {
      notification_type: notificationType,
      notify_before_minutes: notifyBeforeMinutes,
    });
    return response.data;
  },

  updateViewerCount: async (streamId: number, viewerCount: number) => {
    const response = await api.put('/live/streams/' + streamId + '/viewers', null, {
      params: { viewer_count: viewerCount },
    });
    return response.data;
  },
};
