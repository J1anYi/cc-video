import { fetchApi } from './auth';

export interface CommentResponse {
  id: number;
  user_id: number;
  review_id: number;
  username: string;
  content: string;
  created_at: string;
}

export interface CommentListResponse {
  comments: CommentResponse[];
  total: number;
}

export async function createComment(reviewId: number, content: string): Promise<CommentResponse> {
  return fetchApi<CommentResponse>(`/reviews/${reviewId}/comments`, {
    method: 'POST',
    body: JSON.stringify({ content }),
  });
}

export async function getReviewComments(reviewId: number, skip = 0, limit = 20): Promise<CommentListResponse> {
  return fetchApi<CommentListResponse>(`/reviews/${reviewId}/comments?skip=${skip}&limit=${limit}`);
}

export async function deleteComment(commentId: number): Promise<void> {
  await fetchApi(`/comments/${commentId}`, { method: 'DELETE' });
}
