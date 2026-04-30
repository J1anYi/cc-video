import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getNotifications, markNotificationRead, markAllNotificationsRead } from '../api/notifications';
import type { NotificationResponse } from '../api/notifications';

export default function Notifications() {
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    setIsLoading(true);
    try {
      const data = await getNotifications();
      setNotifications(data.notifications);
      setUnreadCount(data.unread_count);
    } catch (err) {
      setError('Failed to load notifications');
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkRead = async (id: number) => {
    try {
      await markNotificationRead(id);
      setNotifications(notifications.map(n => n.id === id ? { ...n, is_read: true } : n));
      setUnreadCount(Math.max(0, unreadCount - 1));
    } catch (err) {
      setError('Failed to mark notification as read');
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await markAllNotificationsRead();
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch (err) {
      setError('Failed to mark all notifications as read');
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  if (isLoading) {
    return <div style={styles.container}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.title}>Notifications</h1>
          {unreadCount > 0 && (
            <button onClick={handleMarkAllRead} style={styles.markAllButton}>
              Mark All Read
            </button>
          )}
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {notifications.length === 0 ? (
          <div style={styles.emptyState}>
            <p>No notifications yet.</p>
          </div>
        ) : (
          <div style={styles.notificationList}>
            {notifications.map((notification) => (
              <div
                key={notification.id}
                style={{
                  ...styles.notificationItem,
                  background: notification.is_read ? '#fff' : '#f0f7ff',
                }}
              >
                <div style={styles.notificationTitle}>{notification.title}</div>
                {notification.content && (
                  <div style={styles.notificationContent}>{notification.content}</div>
                )}
                <div style={styles.notificationTime}>{formatDate(notification.created_at)}</div>
                {!notification.is_read && (
                  <button
                    onClick={() => handleMarkRead(notification.id)}
                    style={styles.markReadButton}
                  >
                    Mark as Read
                  </button>
                )}
              </div>
            ))}
          </div>
        )}

        <button onClick={() => navigate('/movies')} style={styles.backButton}>
          Back to Movies
        </button>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', padding: '2rem', background: '#f5f5f5' },
  card: { background: 'white', padding: '2rem', borderRadius: '8px', maxWidth: '600px', margin: '0 auto' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' },
  title: { margin: 0, fontSize: '1.5rem', color: '#333' },
  markAllButton: { padding: '0.5rem 1rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' },
  emptyState: { textAlign: 'center', padding: '2rem', color: '#666' },
  notificationList: { display: 'flex', flexDirection: 'column', gap: '0.5rem' },
  notificationItem: { padding: '1rem', border: '1px solid #eee', borderRadius: '4px' },
  notificationTitle: { fontWeight: 'bold', color: '#333' },
  notificationContent: { color: '#666', marginTop: '0.25rem' },
  notificationTime: { fontSize: '0.75rem', color: '#999', marginTop: '0.5rem' },
  markReadButton: { marginTop: '0.5rem', padding: '0.25rem 0.5rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem' },
  backButton: { padding: '0.75rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginTop: '1.5rem' },
  error: { padding: '0.75rem', background: '#fee', color: '#c00', borderRadius: '4px', marginBottom: '1rem' },
};
