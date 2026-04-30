import apiClient from "./client";

export interface FeedItem {
  id: number;
  actor_id: number;
  item_type: string;
  item_id: number;
  content?: string;
  movie_id?: number;
  is_read: boolean;
  created_at: string;
}

export interface FeedPreferences {
  show_reviews: boolean;
  show_watchlist: boolean;
  show_favorites: boolean;
  show_discussions: boolean;
  show_achievements: boolean;
}

export interface TrendingItem {
  id: number;
  discussion_type: string;
  discussion_id: number;
  score: number;
}

export interface FollowRecommendation {
  recommended_user_id: number;
  reason: string;
  score: number;
}

export const getSocialFeed = async (): Promise<FeedItem[]> => {
  const response = await apiClient.get<FeedItem[]>("/social-feed");
  return response.data;
};

export const markFeedItemRead = async (feedId: number): Promise<void> => {
  await apiClient.post(`/social-feed/${feedId}/read`);
};

export const markAllFeedRead = async (): Promise<{ marked_count: number }> => {
  const response = await apiClient.post<{ marked_count: number }>("/social-feed/read-all");
  return response.data;
};

export const getFeedPreferences = async (): Promise<FeedPreferences> => {
  const response = await apiClient.get<FeedPreferences>("/social-feed/preferences");
  return response.data;
};

export const updateFeedPreferences = async (prefs: Partial<FeedPreferences>): Promise<void> => {
  await apiClient.put("/social-feed/preferences", prefs);
};

export const getTrendingDiscussions = async (): Promise<TrendingItem[]> => {
  const response = await apiClient.get<TrendingItem[]>("/social-feed/trending");
  return response.data;
};

export const getFollowRecommendations = async (): Promise<FollowRecommendation[]> => {
  const response = await apiClient.get<FollowRecommendation[]>("/social-feed/recommendations");
  return response.data;
};
