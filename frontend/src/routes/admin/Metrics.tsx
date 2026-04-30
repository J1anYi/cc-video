import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getOverview, getTrending, getRankings, getRetention } from '../../api/adminMetrics';
import type { PlatformOverview, TrendingItem, RankingItem, RetentionMetrics } from '../../api/adminMetrics';

export default function AdminMetrics() {
  const [overview, setOverview] = useState<PlatformOverview | null>(null);
  const [trending, setTrending] = useState<TrendingItem[]>([]);
  const [rankings, setRankings] = useState<RankingItem[]>([]);
  const [retention, setRetention] = useState<RetentionMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('week');
  const [sortBy, setSortBy] = useState('views');

  useEffect(() => {
    loadMetrics();
  }, [period, sortBy]);

  const loadMetrics = async () => {
    setLoading(true);
    try {
      const [overviewData, trendingData, rankingsData, retentionData] = await Promise.all([
        getOverview(),
        getTrending(period),
        getRankings({ sort_by: sortBy }),
        getRetention()
      ]);
      setOverview(overviewData);
      setTrending(trendingData);
      setRankings(rankingsData);
      setRetention(retentionData);
    } catch (error) {
      console.error('Failed to load metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-400">Loading metrics...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-white mb-8">Platform Metrics</h1>

      {/* Overview Cards */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-blue-400">{overview.total_views}</div>
            <div className="text-gray-400 text-sm">Total Views</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-green-400">{overview.active_users}</div>
            <div className="text-gray-400 text-sm">Active Users</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-purple-400">{overview.total_users}</div>
            <div className="text-gray-400 text-sm">Total Users</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-yellow-400">{overview.total_movies}</div>
            <div className="text-gray-400 text-sm">Movies</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-pink-400">{overview.total_watch_time_hours}</div>
            <div className="text-gray-400 text-sm">Hours Watched</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-cyan-400">{overview.engagement_rate}%</div>
            <div className="text-gray-400 text-sm">Engagement</div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Trending Content */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-white">Trending Content</h2>
            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="bg-gray-700 text-white rounded px-3 py-1 text-sm"
            >
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="all">All Time</option>
            </select>
          </div>
          <div className="space-y-2">
            {trending.map((item, i) => (
              <Link
                key={item.id}
                to={`/movies/${item.id}`}
                className="flex items-center justify-between p-2 hover:bg-gray-700 rounded"
              >
                <div className="flex items-center gap-3">
                  <span className="text-gray-500 w-6">{i + 1}</span>
                  <div>
                    <div className="text-white">{item.title}</div>
                    <div className="text-gray-500 text-sm">{item.genre}</div>
                  </div>
                </div>
                <div className="text-blue-400">{item.views} views</div>
              </Link>
            ))}
          </div>
        </div>

        {/* Retention */}
        {retention && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-white mb-4">User Retention</h2>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-400">New Users (30d)</span>
                <span className="text-white font-medium">{retention.new_users_30d}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Returning (7d)</span>
                <span className="text-white font-medium">{retention.returning_users_7d}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Retention Rate</span>
                <span className="text-green-400 font-medium">{retention.retention_rate}%</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Content Rankings */}
      <div className="bg-gray-800 rounded-lg p-6 mt-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-white">Content Rankings</h2>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
              className="bg-gray-700 text-white rounded px-3 py-1 text-sm"
          >
            <option value="views">By Views</option>
            <option value="rating">By Rating</option>
            <option value="recent">Most Recent</option>
          </select>
        </div>
        <table className="w-full">
          <thead>
            <tr className="text-gray-400 text-sm">
              <th className="text-left py-2">Title</th>
              <th className="text-left py-2">Genre</th>
              <th className="text-right py-2">Views</th>
              <th className="text-right py-2">Rating</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((item) => (
              <tr key={item.id} className="border-t border-gray-700">
                <td className="py-2">
                  <Link to={`/movies/${item.id}`} className="text-white hover:text-blue-400">
                    {item.title}
                  </Link>
                </td>
                <td className="py-2 text-gray-400">{item.genre}</td>
                <td className="py-2 text-right text-blue-400">{item.views}</td>
                <td className="py-2 text-right text-yellow-400">
                  {item.avg_rating ? item.avg_rating.toFixed(1) : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
