import apiClient from "./client";

export interface Badge {
  id: number;
  name: string;
  description: string;
  icon: string;
  badge_type: string;
  xp_reward: number;
}

export interface UserXP {
  total_xp: number;
  level: number;
}

export interface LeaderboardEntry {
  user_id: number;
  score: number;
  rank: number;
}

export interface Challenge {
  id: number;
  title: string;
  description: string;
  xp_reward: number;
  requirement_count: number;
}

export interface UserChallenge {
  challenge_id: number;
  progress: number;
  is_completed: boolean;
}

export interface Reward {
  id: number;
  name: string;
  description: string;
  level_required: number;
}

export const getBadges = async (): Promise<Badge[]> => {
  const response = await apiClient.get<Badge[]>("/gamification/badges");
  return response.data;
};

export const getMyBadges = async (): Promise<{ badge_id: number; earned_at: string }[]> => {
  const response = await apiClient.get("/gamification/badges/my");
  return response.data;
};

export const getXP = async (): Promise<UserXP> => {
  const response = await apiClient.get<UserXP>("/gamification/xp");
  return response.data;
};

export const addXP = async (amount: number): Promise<UserXP> => {
  const response = await apiClient.post<UserXP>("/gamification/xp", { amount });
  return response.data;
};

export const getLeaderboard = async (category: string): Promise<LeaderboardEntry[]> => {
  const response = await apiClient.get<LeaderboardEntry[]>(`/gamification/leaderboard/${category}`);
  return response.data;
};

export const getChallenges = async (): Promise<Challenge[]> => {
  const response = await apiClient.get<Challenge[]>("/gamification/challenges");
  return response.data;
};

export const getMyChallenges = async (): Promise<UserChallenge[]> => {
  const response = await apiClient.get<UserChallenge[]>("/gamification/challenges/my");
  return response.data;
};

export const joinChallenge = async (challengeId: number): Promise<void> => {
  await apiClient.post(`/gamification/challenges/${challengeId}/join`);
};

export const updateChallengeProgress = async (challengeId: number, progress: number): Promise<void> => {
  await apiClient.post(`/gamification/challenges/${challengeId}/progress`, { progress });
};

export const getRewards = async (): Promise<Reward[]> => {
  const response = await apiClient.get<Reward[]>("/gamification/rewards");
  return response.data;
};

export const getMyRewards = async (): Promise<{ reward_id: number; unlocked_at: string }[]> => {
  const response = await apiClient.get("/gamification/rewards/my");
  return response.data;
};

export const unlockReward = async (rewardId: number): Promise<void> => {
  await apiClient.post(`/gamification/rewards/${rewardId}/unlock`);
};
