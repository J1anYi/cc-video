import api from './client';

export interface Forum {
  id: number;
  name: string;
  slug: string;
  description?: string;
  category: string;
  thread_count: number;
}

export interface ForumThread {
  id: number;
  title: string;
  forum_id: number;
  author_id: number;
  is_pinned: boolean;
  reply_count: number;
  view_count: number;
  last_post_at?: string;
  created_at: string;
}

export interface ForumPost {
  id: number;
  author_id: number;
  content: string;
  helpful_count: number;
  created_at: string;
}

export const forumApi = {
  getForums: async () => {
    const response = await api.get('/forums');
    return response.data.forums as Forum[];
  },

  createForum: async (data: { name: string; slug: string; description?: string; category?: string }) => {
    const response = await api.post('/forums', data);
    return response.data;
  },

  getForumThreads: async (forumId: number, skip = 0, limit = 20) => {
    const response = await api.get('/forums/' + forumId + '/threads', { params: { skip, limit } });
    return response.data.threads as ForumThread[];
  },

  createThread: async (data: { forum_id: number; title: string; content: string }) => {
    const response = await api.post('/forums/threads', data);
    return response.data;
  },

  searchThreads: async (query: string, skip = 0, limit = 20) => {
    const response = await api.get('/forums/threads/search', { params: { q: query, skip, limit } });
    return response.data.threads as ForumThread[];
  },

  getThreadPosts: async (threadId: number, skip = 0, limit = 50) => {
    const response = await api.get('/forums/threads/' + threadId, { params: { skip, limit } });
    return response.data.posts as ForumPost[];
  },

  createPost: async (threadId: number, content: string) => {
    const response = await api.post('/forums/threads/' + threadId + '/posts', { content });
    return response.data;
  },

  moderate: async (data: { action: string; target_type: string; target_id: number; reason?: string }) => {
    const response = await api.post('/forums/moderate', data);
    return response.data;
  },
};
