import apiClient from "./client";

export interface Group {
  id: number;
  name: string;
  slug: string;
  description?: string;
  privacy: string;
  member_count: number;
}

export interface GroupMember {
  user_id: number;
  role: string;
  joined_at: string;
}

export interface GroupCollection {
  id: number;
  name: string;
  description?: string;
  item_count: number;
}

export interface GroupCollectionItem {
  id: number;
  collection_id: number;
  movie_id: number;
  added_by: number;
  added_at: string;
}

export interface GroupDiscussion {
  id: number;
  title: string;
  author_id: number;
  reply_count: number;
  is_pinned: boolean;
  created_at: string;
}

export interface GroupDiscussionReply {
  id: number;
  discussion_id: number;
  author_id: number;
  content: string;
  created_at: string;
}

export interface GroupActivity {
  id: number;
  user_id: number;
  activity_type: string;
  content: string;
  created_at: string;
}

export interface CreateGroupRequest {
  name: string;
  slug: string;
  description?: string;
  privacy?: string;
}

export interface UpdateGroupRequest {
  name?: string;
  description?: string;
  privacy?: string;
}

export interface CreateCollectionRequest {
  name: string;
  description?: string;
}

export interface CreateDiscussionRequest {
  title: string;
  content: string;
}


export const createGroup = async (data: CreateGroupRequest): Promise<Group> => {
  const response = await apiClient.post<Group>("/groups", data);
  return response.data;
};

export const getGroups = async (): Promise<Group[]> => {
  const response = await apiClient.get<Group[]>("/groups");
  return response.data;
};

export const getGroup = async (id: number): Promise<Group> => {
  const response = await apiClient.get<Group>(`/groups/${id}`);
  return response.data;
};

export const updateGroup = async (id: number, data: UpdateGroupRequest): Promise<Group> => {
  const response = await apiClient.put<Group>(`/groups/${id}`, data);
  return response.data;
};

export const deleteGroup = async (id: number): Promise<void> => {
  await apiClient.delete(`/groups/${id}`);
};

export const joinGroup = async (id: number): Promise<void> => {
  await apiClient.post(`/groups/${id}/join`);
};

export const leaveGroup = async (id: number): Promise<void> => {
  await apiClient.post(`/groups/${id}/leave`);
};

export const inviteMember = async (groupId: number, userId: number): Promise<void> => {
  await apiClient.post(`/groups/${groupId}/invite`, { user_id: userId });
};

export const getMembers = async (groupId: number): Promise<GroupMember[]> => {
  const response = await apiClient.get<GroupMember[]>(`/groups/${groupId}/members`);
  return response.data;
};

export const updateMemberRole = async (groupId: number, userId: number, role: string): Promise<void> => {
  await apiClient.put(`/groups/${groupId}/members/${userId}`, { role });
};

export const removeMember = async (groupId: number, userId: number): Promise<void> => {
  await apiClient.delete(`/groups/${groupId}/members/${userId}`);
};

export const getCollections = async (groupId: number): Promise<GroupCollection[]> => {
  const response = await apiClient.get<GroupCollection[]>(`/groups/${groupId}/collections`);
  return response.data;
};

export const createCollection = async (groupId: number, data: CreateCollectionRequest): Promise<GroupCollection> => {
  const response = await apiClient.post<GroupCollection>(`/groups/${groupId}/collections`, data);
  return response.data;
};

export const addCollectionItem = async (groupId: number, collectionId: number, movieId: number): Promise<void> => {
  await apiClient.post(`/groups/${groupId}/collections/${collectionId}/items`, { movie_id: movieId });
};

export const removeCollectionItem = async (groupId: number, collectionId: number, itemId: number): Promise<void> => {
  await apiClient.delete(`/groups/${groupId}/collections/${collectionId}/items/${itemId}`);
};

export const getDiscussions = async (groupId: number): Promise<GroupDiscussion[]> => {
  const response = await apiClient.get<GroupDiscussion[]>(`/groups/${groupId}/discussions`);
  return response.data;
};

export const createDiscussion = async (groupId: number, data: CreateDiscussionRequest): Promise<GroupDiscussion> => {
  const response = await apiClient.post<GroupDiscussion>(`/groups/${groupId}/discussions`, data);
  return response.data;
};

export const createDiscussionReply = async (groupId: number, discussionId: number, content: string): Promise<GroupDiscussionReply> => {
  const response = await apiClient.post<GroupDiscussionReply>(`/groups/${groupId}/discussions/${discussionId}/replies`, { content });
  return response.data;
};

export const getActivityFeed = async (groupId: number): Promise<GroupActivity[]> => {
  const response = await apiClient.get<GroupActivity[]>(`/groups/${groupId}/activity`);
  return response.data;
};
