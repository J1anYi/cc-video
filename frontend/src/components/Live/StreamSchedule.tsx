import React, { useState } from 'react';
import { livestreamApi, ScheduledStream } from '../../api/livestream';

export const StreamSchedule: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [scheduledStart, setScheduledStart] = useState('');
  const [isRecurring, setIsRecurring] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await livestreamApi.scheduleStream({
        title,
        description,
        scheduled_start: scheduledStart,
        is_recurring: isRecurring,
      });
      setTitle('');
      setDescription('');
      setScheduledStart('');
      alert('Stream scheduled successfully!');
    } catch (error) {
      console.error('Failed to schedule stream:', error);
      alert('Failed to schedule stream');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stream-schedule">
      <h2>Schedule a Live Stream</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div>
          <label>Scheduled Start</label>
          <input
            type="datetime-local"
            value={scheduledStart}
            onChange={(e) => setScheduledStart(e.target.value)}
            required
          />
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              checked={isRecurring}
              onChange={(e) => setIsRecurring(e.target.checked)}
            />
            Recurring
          </label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Scheduling...' : 'Schedule Stream'}
        </button>
      </form>
    </div>
  );
};

export const UpcomingStreams: React.FC = () => {
  const [streams, setStreams] = useState<ScheduledStream[]>([]);
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const fetchStreams = async () => {
      try {
        const data = await livestreamApi.getUpcomingStreams();
        setStreams(data);
      } catch (error) {
        console.error('Failed to fetch upcoming streams:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStreams();
  }, []);

  if (loading) return <div>Loading upcoming streams...</div>;

  return (
    <div className="upcoming-streams">
      <h2>Upcoming Streams</h2>
      {streams.length === 0 ? (
        <p>No upcoming streams</p>
      ) : (
        <ul>
          {streams.map((stream) => (
            <li key={stream.id}>
              <h3>{stream.title}</h3>
              <p>{stream.description}</p>
              <small>Starts: {new Date(stream.scheduled_start).toLocaleString()}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
