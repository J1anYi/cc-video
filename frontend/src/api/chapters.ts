import api from './client';

export interface VideoChapter {
  id: number;
  title: string;
  start_time: number;
  end_time?: number;
  thumbnail_path?: string;
}

export interface UserBookmark {
  id: number;
  movie_id: number;
  timestamp: number;
  note?: string;
}

export const chapterApi = {
  getMovieChapters: async (movieId: number) => {
    const response = await api.get('/chapters/movie/' + movieId);
    return response.data.chapters as VideoChapter[];
  },

  createChapter: async (data: {
    movie_id: number;
    title: string;
    start_time: number;
    end_time?: number;
    thumbnail_path?: string;
  }) => {
    const response = await api.post('/chapters', data);
    return response.data;
  },

  updateChapter: async (chapterId: number, data: Partial<{
    title: string;
    start_time: number;
    end_time: number;
    thumbnail_path: string;
  }>) => {
    const response = await api.put('/chapters/' + chapterId, data);
    return response.data;
  },

  deleteChapter: async (chapterId: number) => {
    const response = await api.delete('/chapters/' + chapterId);
    return response.data;
  },

  getBookmarks: async (movieId?: number) => {
    const response = await api.get('/chapters/bookmarks', {
      params: movieId ? { movie_id: movieId } : {},
    });
    return response.data.bookmarks as UserBookmark[];
  },

  createBookmark: async (data: {
    movie_id: number;
    timestamp: number;
    note?: string;
  }) => {
    const response = await api.post('/chapters/bookmarks', data);
    return response.data;
  },

  deleteBookmark: async (bookmarkId: number) => {
    const response = await api.delete('/chapters/bookmarks/' + bookmarkId);
    return response.data;
  },
};
