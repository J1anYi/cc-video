import apiClient from "./client";

export interface WatchParty {
  id: number;
  title: string;
  movie_id: number;
  status: string;
  scheduled_start: string;
  participant_count: number;
}

export interface WatchPartyParticipant {
  user_id: number;
  role: string;
  playback_position: number;
}

export interface WatchPartyChat {
  id: number;
  user_id: number;
  message: string;
  playback_time: number;
  created_at: string;
}

export interface CreateWatchPartyRequest {
  title: string;
  movie_id: number;
  scheduled_start: string;
  description?: string;
  is_public?: boolean;
  max_participants?: number;
}

export const createWatchParty = async (data: CreateWatchPartyRequest): Promise<WatchParty> => {
  const response = await apiClient.post<WatchParty>("/watch-parties", data);
  return response.data;
};

export const getUpcomingWatchParties = async (): Promise<WatchParty[]> => {
  const response = await apiClient.get<WatchParty[]>("/watch-parties");
  return response.data;
};

export const getMyWatchParties = async (): Promise<WatchParty[]> => {
  const response = await apiClient.get<WatchParty[]>("/watch-parties/my");
  return response.data;
};

export const getWatchParty = async (id: number): Promise<WatchParty> => {
  const response = await apiClient.get<WatchParty>(`/watch-parties/${id}`);
  return response.data;
};

export const joinWatchParty = async (id: number): Promise<void> => {
  await apiClient.post(`/watch-parties/${id}/join`);
};

export const leaveWatchParty = async (id: number): Promise<void> => {
  await apiClient.post(`/watch-parties/${id}/leave`);
};

export const getWatchPartyParticipants = async (id: number): Promise<WatchPartyParticipant[]> => {
  const response = await apiClient.get<WatchPartyParticipant[]>(`/watch-parties/${id}/participants`);
  return response.data;
};

export const inviteToWatchParty = async (partyId: number, userId: number): Promise<void> => {
  await apiClient.post(`/watch-parties/${partyId}/invite`, { user_id: userId });
};

export const sendWatchPartyChat = async (partyId: number, message: string, playbackTime: number = 0): Promise<void> => {
  await apiClient.post(`/watch-parties/${partyId}/chat`, { message, playback_time: playbackTime });
};

export const getWatchPartyChat = async (partyId: number): Promise<WatchPartyChat[]> => {
  const response = await apiClient.get<WatchPartyChat[]>(`/watch-parties/${partyId}/chat`);
  return response.data;
};
