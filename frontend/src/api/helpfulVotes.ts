import { fetchApi } from './auth';

export interface HelpfulVoteResponse {
  review_id: number;
  helpful_count: number;
  user_voted: boolean;
}

export interface HelpfulVoteToggleResponse {
  review_id: number;
  helpful_count: number;
  voted: boolean;
}

export async function toggleHelpful(reviewId: number): Promise<HelpfulVoteToggleResponse> {
  return fetchApi<HelpfulVoteToggleResponse>(`/reviews/${reviewId}/helpful`, {
    method: 'POST',
  });
}

export async function getHelpfulStatus(reviewId: number): Promise<HelpfulVoteResponse> {
  return fetchApi<HelpfulVoteResponse>(`/reviews/${reviewId}/helpful`);
}
