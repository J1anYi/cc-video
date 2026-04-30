import { useState, useEffect } from 'react';
import {
  getUserJourney,
  getSessionMetrics,
  getCohortAnalytics,
  getChurnRiskUsers,
  type UserJourney,
  type SessionMetrics,
  type Cohort,
  type ChurnRiskUser,
} from '../../api/userBehavior';
import CohortTable from '../../components/analytics/CohortTable';
import ChurnRiskList from '../../components/analytics/ChurnRiskList';

type Tab = 'journeys' | 'sessions' | 'cohorts' | 'churn';

export default function UserBehavior() {
  const [activeTab, setActiveTab] = useState<Tab>('cohorts');
  const [userIdInput, setUserIdInput] = useState('');
  const [journey, setJourney] = useState<UserJourney | null>(null);
  const [sessionMetrics, setSessionMetrics] = useState<SessionMetrics | null>(null);
  const [cohorts, setCohorts] = useState<Cohort[]>([]);
  const [churnUsers, setChurnUsers] = useState<ChurnRiskUser[]>([]);
  const [churnThreshold, setChurnThreshold] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (activeTab === 'cohorts') loadCohorts();
    if (activeTab === 'churn') loadChurnUsers();
  }, [activeTab, churnThreshold]);

  const loadJourney = async () => {
    if (!userIdInput) return;
    try {
      setLoading(true);
      const data = await getUserJourney(parseInt(userIdInput, 10));
      setJourney(data);
    } catch (err) {
      setError('Failed to load user journey');
    } finally {
      setLoading(false);
    }
  };

  const loadSessionMetrics = async () => {
    try {
      setLoading(true);
      const data = await getSessionMetrics();
      setSessionMetrics(data);
    } catch (err) {
      setError('Failed to load session metrics');
    } finally {
      setLoading(false);
    }
  };

  const loadCohorts = async () => {
    try {
      setLoading(true);
      const data = await getCohortAnalytics(12);
      setCohorts(data);
    } catch (err) {
      setError('Failed to load cohorts');
    } finally {
      setLoading(false);
    }
  };

  const loadChurnUsers = async () => {
    try {
      setLoading(true);
      const data = await getChurnRiskUsers(churnThreshold, 50);
      setChurnUsers(data);
    } catch (err) {
      setError('Failed to load churn data');
    } finally {
      setLoading(false);
    }
  };

  const tabs: { key: Tab; label: string }[] = [
    { key: 'journeys', label: 'Journeys' },
    { key: 'sessions', label: 'Sessions' },
    { key: 'cohorts', label: 'Cohorts' },
    { key: 'churn', label: 'Churn Risk' },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">User Behavior Analytics</h1>

      <div className="flex gap-2 mb-6 border-b border-gray-700 pb-2">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-4 py-2 rounded-t ${
              activeTab === tab.key ? 'bg-blue-600 text-white' : 'bg-gray-800 hover:bg-gray-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {error && <div className="bg-red-900 text-red-200 p-4 rounded mb-4">{error}</div>}

      {activeTab === 'journeys' && (
        <div>
          <div className="flex gap-4 mb-4">
            <input
              type="number"
              placeholder="User ID"
              value={userIdInput}
              onChange={(e) => setUserIdInput(e.target.value)}
              className="bg-gray-800 px-4 py-2 rounded w-48"
            />
            <button onClick={loadJourney} className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700">
              Load Journey
            </button>
          </div>
          {journey && (
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold mb-4">User {journey.user_id} - {journey.total_events} events</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {journey.events.map((event) => (
                  <div key={event.id} className="bg-gray-700 p-3 rounded text-sm">
                    <div className="flex justify-between">
                      <span className="font-medium">{event.event_type}</span>
                      <span className="text-gray-400">{new Date(event.created_at).toLocaleString()}</span>
                    </div>
                    <div className="text-gray-300 mt-1 truncate">{event.page_url}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'sessions' && (
        <div>
          <button onClick={loadSessionMetrics} className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 mb-4">
            Load Session Metrics
          </button>
          {sessionMetrics && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-3xl font-bold">{sessionMetrics.total_sessions}</div>
                <div className="text-gray-400 text-sm">Total Sessions</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-3xl font-bold">{Math.floor(sessionMetrics.avg_duration_seconds / 60)}m</div>
                <div className="text-gray-400 text-sm">Avg Duration</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-3xl font-bold">{sessionMetrics.bounce_rate.toFixed(1)}%</div>
                <div className="text-gray-400 text-sm">Bounce Rate</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-3xl font-bold">{sessionMetrics.peak_hour}:00</div>
                <div className="text-gray-400 text-sm">Peak Hour</div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'cohorts' && (
        <div>{loading ? <div className="text-gray-400">Loading cohorts...</div> : <CohortTable cohorts={cohorts} />}</div>
      )}

      {activeTab === 'churn' && (
        <div>
          <div className="mb-4">
            <label className="text-gray-400 mr-2">Risk Threshold:</label>
            <input
              type="range"
              min="0"
              max="100"
              value={churnThreshold}
              onChange={(e) => setChurnThreshold(parseInt(e.target.value, 10))}
              className="w-48"
            />
            <span className="ml-2">{churnThreshold}%</span>
          </div>
          {loading ? (
            <div className="text-gray-400">Loading churn data...</div>
          ) : (
            <ChurnRiskList users={churnUsers} threshold={churnThreshold} onThresholdChange={setChurnThreshold} />
          )}
        </div>
      )}
    </div>
  );
}
