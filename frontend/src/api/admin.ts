import type { Movie, MovieListResponse, CreateMovieRequest, UpdateMovieRequest } from './types';
import { fetchApi } from './auth';

// Admin Movies API
export async function getAdminMovies(): Promise<MovieListResponse> {
  return fetchApi<MovieListResponse>('/admin/movies');
}

export async function getAdminMovie(id: number): Promise<Movie> {
  return fetchApi<Movie>(`/admin/movies/${id}`);
}

export async function createMovie(data: CreateMovieRequest): Promise<Movie> {
  return fetchApi<Movie>('/admin/movies', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateMovie(id: number, data: UpdateMovieRequest): Promise<Movie> {
  return fetchApi<Movie>(`/admin/movies/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteMovie(id: number): Promise<void> {
  return fetchApi<void>(`/admin/movies/${id}`, {
    method: 'DELETE',
  });
}

export async function uploadVideo(movieId: number, file: File): Promise<void> {
  const token = localStorage.getItem('token');
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`/api/v1/admin/movies/${movieId}/video`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(error.detail || 'Upload failed');
  }
}
