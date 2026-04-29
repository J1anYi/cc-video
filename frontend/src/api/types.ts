// API Types
export interface User {
  id: number;
  username: string;
  role: 'admin' | 'user';
}

export interface Movie {
  id: number;
  title: string;
  description: string | null;
  category: string | null;
  poster_path: string | null;
  publication_status: 'DRAFT' | 'PUBLISHED' | 'UNPUBLISHED' | 'DISABLED';
  created_at: string;
  updated_at: string;
}

export interface MovieListResponse {
  movies: Movie[];
  total: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface CreateMovieRequest {
  title: string;
  description?: string;
  publication_status?: 'DRAFT' | 'PUBLISHED' | 'UNPUBLISHED' | 'DISABLED';
}

export interface UpdateMovieRequest {
  title?: string;
  description?: string;
  publication_status?: 'DRAFT' | 'PUBLISHED' | 'UNPUBLISHED' | 'DISABLED';
}

export interface WatchHistory {
  id: number;
  movie_id: number;
  progress: number;
  last_watched_at: string;
  movie: Movie | null;
}

export interface WatchHistoryUpdate {
  movie_id: number;
  progress: number;
}

export interface Favorite {
  id: number;
  movie_id: number;
  created_at: string;
  movie: Movie | null;
}

export interface FavoriteStatus {
  is_favorite: boolean;
}
