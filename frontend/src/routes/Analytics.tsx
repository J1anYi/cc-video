import { useState, useEffect } from 'react';
import { getAnalytics, exportData } from '../api/analytics';
import type { AnalyticsData } from '../api/analytics';

export default function Analytics() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async (refresh = false) => {
    setLoading(true);
    try {
      const data = await getAnalytics(refresh);
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: 'json' | 'csv') => {
    setExporting(true);
    try {
      const blob = await exportData(format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `viewing_data.${format}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8">
        <div className="text-center text-gray-400">Loading analytics...</div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="p-8">
        <div className="text-center text-gray-400">No analytics data available</div>
      </div>
    );
  }

  const genreLabels = Object.keys(analytics.genre_breakdown);
  const genreValues = Object.values(analytics.genre_breakdown);
  const totalGenreCount = genreValues.reduce((a, b) => a + b, 0);
  const maxGenreValue = Math.max(...genreValues, 1);

  const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  const dailyValues = days.map(d => analytics.daily_pattern[d] || 0);
  const maxDailyValue = Math.max(...dailyValues, 1);

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">My Analytics</h1>
        <div className="flex gap-2">
          <button
            onClick={() => loadAnalytics(true)}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm"
          >
            Refresh
          </button>
          <button
            onClick={() => handleExport('json')}
            disabled={exporting}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm disabled:opacity-50"
          >
            Export JSON
          </button>
          <button
            onClick={() => handleExport('csv')}
            disabled={exporting}
            className="px-4 py-2 bg-green-600 hover:bg-green-500 rounded text-sm disabled:opacity-50"
          >
            Export CSV
          </button>
        </div>
      </div>

      {/* Watch Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-300">Watch Time</h2>
          <div className="text-5xl font-bold text-blue-400 mb-2">
            {analytics.watch_time.total_hours}
          </div>
          <div className="text-gray-400">hours watched</div>
          <div className="mt-4 text-lg text-gray-300">
            <span className="text-green-400">{analytics.watch_time.total_movies}</span> movies
          </div>
        </div>

        {/* Genre Breakdown */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-300">Genre Preferences</h2>
          {genreLabels.length > 0 ? (
            <div className="space-y-2">
              {genreLabels.slice(0, 5).map((genre) => (
                <div key={genre}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-300">{genre}</span>
                    <span className="text-gray-400">
                      {analytics.genre_breakdown[genre]} ({Math.round(analytics.genre_breakdown[genre] / totalGenreCount * 100)}%)
                    </span>
                  </div>
                  <div className="h-2 bg-gray-700 rounded">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded"
                      style={{ width: `${(analytics.genre_breakdown[genre] / maxGenreValue) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-gray-400">No genre data yet</div>
          )}
        </div>
      </div>

      {/* Daily Pattern */}
      <div className="bg-gray-800 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-300">Weekly Viewing Pattern</h2>
        <div className="flex items-end justify-between h-40 gap-2">
          {days.map((day, i) => (
            <div key={day} className="flex-1 flex flex-col items-center">
              <div className="w-full flex-1 flex items-end">
                <div
                  className="w-full bg-gradient-to-t from-blue-600 to-blue-400 rounded-t"
                  style={{ height: `${(dailyValues[i] / maxDailyValue) * 100}%`, minHeight: '4px' }}
                />
              </div>
              <div className="text-xs text-gray-400 mt-2 capitalize">{day.slice(0, 3)}</div>
              <div className="text-xs text-gray-500">{dailyValues[i]}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Hourly Pattern */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-300">Hourly Viewing Pattern</h2>
        <div className="flex items-end justify-between h-24 gap-1">
          {Array.from({ length: 24 }, (_, h) => {
            const count = analytics.hourly_pattern[h.toString()] || 0;
            const maxHourly = Math.max(...Object.values(analytics.hourly_pattern), 1);
            return (
              <div key={h} className="flex-1 flex flex-col items-center">
                <div
                  className="w-full bg-blue-500 rounded-t"
                  style={{ height: `${(count / maxHourly) * 100}%`, minHeight: count > 0 ? '2px' : '0' }}
                />
                {h % 6 === 0 && (
                  <div className="text-xs text-gray-500 mt-1">{h}:00</div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {analytics.last_updated && (
        <div className="text-center text-gray-500 text-sm mt-8">
          Last updated: {new Date(analytics.last_updated).toLocaleString()}
        </div>
      )}
    </div>
  );
}
