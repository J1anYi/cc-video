import { fetchApi } from './auth';

export interface NotificationResponse {
  id: number;
  notification_type: string;
  title: string;
  content: string | null;
  actor_id: number | null;
  actor_name: string | null;
  target_type: string | null;
  target_id: number | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  notifications: NotificationResponse[];
  total: number;
  unread_count: number;
}

export interface UnreadCountResponse {
  unread_count: number;
}

export async function getNotifications(skip = 0, limit = 20, unreadOnly = false): Promise<NotificationListResponse> {
  return fetchApi<NotificationListResponse>(`/notifications?skip=${skip}&limit=${limit}&unread_only=${unreadOnly}`);
}

export async function markNotificationRead(notificationId: number): Promise<void> {
  await fetchApi(`/notifications/${notificationId}/read`, { method: 'PATCH' });
}

export async function markAllNotificationsRead(): Promise<void> {
  await fetchApi('/notifications/read-all', { method: 'PATCH' });
}

export async function getUnreadCount(): Promise<UnreadCountResponse> {
  return fetchApi<UnreadCountResponse>('/notifications/unread-count');
}
