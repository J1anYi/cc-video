import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { adminDashboardApi, DashboardData } from '../../api/adminDashboard';

export default function AdminDashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const dashboardData = await adminDashboardApi.getDashboard();
      setData(dashboardData);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-400">Loading dashboard...</div>;
  }

  if (!data) {
    return <div className="p-8 text-center text-gray-400">No data available</div>;
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'watch': return '🎬';
      case 'rating': return '⭐';
      case 'review': return '📝';
      case 'comment': return '💬';
      case 'follow': return '👤';
      default: return '📌';
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">Admin Dashboard</h1>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <Link to="/admin/users" className="bg-gray-800 rounded-lg p-4 hover:bg-gray-700">
          <div className="text-3xl font-bold text-blue-400">{data.metrics.total_users}</div>
          <div className="text-gray-400 text-sm">Total Users</div>
          <div className="text-green-400 text-xs mt-1">+{data.metrics.new_users_today} today</div>
        </Link>
        <Link to="/admin/movies" className="bg-gray-800 rounded-lg p-4 hover:bg-gray-700">
          <div className="text-3xl font-bold text-purple-400">{data.metrics.total_movies}</div>
          <div className="text-gray-400 text-sm">Movies</div>
        </Link>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="text-3xl font-bold text-green-400">{data.metrics.views_today}</div>
          <div className="text-gray-400 text-sm">Views Today</div>
        </div>
        <Link to="/admin/reports" className="bg-gray-800 rounded-lg p-4 hover:bg-gray-700">
          <div className="text-3xl font-bold text-yellow-400">{data.metrics.pending_reports}</div>
          <div className="text-gray-400 text-sm">Pending Reports</div>
        </Link>
        <Link to="/admin/metrics" className="bg-gray-800 rounded-lg p-4 hover:bg-gray-700">
          <div className="text-3xl font-bold text-cyan-400">{data.growth.growth_rate}%</div>
          <div className="text-gray-400 text-sm">User Growth</div>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Activity Feed */}
        <div className="lg:col-span-2 bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Recent Activity</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {data.activity.length > 0 ? (
              data.activity.map((item) => (
                <div key={item.id} className="flex items-center gap-3 p-2 hover:bg-gray-700 rounded">
                  <span className="text-lg">{getActivityIcon(item.type)}</span>
                  <div className="flex-1">
                    <span className="text-gray-300 capitalize">{item.type}</span>
                    {item.movie_id && (
                      <Link to={"/movies/" + item.movie_id} className="text-blue-400 ml-2">
                        movie #{item.movie_id}
                      </Link>
                    )}
                  </div>
                  <span className="text-gray-500 text-xs">
                    {new Date(item.created_at).toLocaleTimeString()}
                  </span>
                </div>
              ))
            ) : (
              <div className="text-gray-500 text-center py-4">No recent activity</div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Quick Actions</h2>
          <div className="space-y-2">
            <Link to="/admin/movies/new" className="block bg-blue-600 hover:bg-blue-500 text-white text-center py-2 rounded">
              Add Movie
            </Link>
            <Link to="/admin/reports" className="block bg-yellow-600 hover:bg-yellow-500 text-white text-center py-2 rounded">
              Review Reports ({data.health.pending_reports})
            </Link>
            <Link to="/admin/users" className="block bg-purple-600 hover:bg-purple-500 text-white text-center py-2 rounded">
              Manage Users
            </Link>
            <Link to="/admin/metrics" className="block bg-green-600 hover:bg-green-500 text-white text-center py-2 rounded">
              View Analytics
            </Link>
          </div>

          {/* Content Health */}
          <h3 className="text-lg font-semibold text-white mt-6 mb-3">Content Health</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Pending Reports</span>
              <span className={data.health.pending_reports > 0 ? 'text-yellow-400' : 'text-green-400'}>
                {data.health.pending_reports}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Stale Content</span>
              <span className="text-gray-300">{data.health.stale_content}</span>
            </div>
          </div>
        </div>
      </div>

      {/* User Growth Chart */}
      <div className="bg-gray-800 rounded-lg p-6 mt-8">
        <h2 className="text-xl font-semibold text-white mb-4">User Growth (Last 7 Days)</h2>
        <div className="flex items-end justify-between h-32 gap-2">
          {data.growth.daily.map((day) => {
            const maxCount = Math.max(...data.growth.daily.map(d => d.count), 1);
            return (
              <div key={day.date} className="flex-1 flex flex-col items-center">
                <div className="w-full flex-1 flex items-end">
                  <div
                    className="w-full bg-gradient-to-t from-blue-600 to-blue-400 rounded-t"
                    style={{ height: ((day.count / maxCount) * 100) + '%', minHeight: '4px' }}
                  />
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {new Date(day.date).toLocaleDateString('en', { weekday: 'short' })}
                </div>
                <div className="text-xs text-gray-400">{day.count}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
