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
