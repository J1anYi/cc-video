import { useState, useEffect } from 'react';
import {
  getTrendingContent,
  getContentMetrics,
  getContentHeatmap,
  getCompletionAnalysis,
  compareContent,
  type TrendingContent,
  type ContentMetrics,
  type HeatmapData,
  type CompletionAnalysis,
} from '../../api/contentAnalytics';
import EngagementHeatmap from '../../components/analytics/EngagementHeatmap';
import CompletionChart from '../../components/analytics/CompletionChart';

export default function ContentAnalytics() {
  const [trending, setTrending] = useState<TrendingContent[]>([]);
  const [selectedContentId, setSelectedContentId] = useState<number | null>(null);
  const [metrics, setMetrics] = useState<ContentMetrics | null>(null);
  const [heatmap, setHeatmap] = useState<HeatmapData | null>(null);
  const [completion, setCompletion] = useState<CompletionAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTrending();
  }, []);

  useEffect(() => {
    if (selectedContentId) {
      loadContentDetails(selectedContentId);
    }
  }, [selectedContentId]);

  const loadTrending = async () => {
    try {
      setLoading(true);
      const response = await getTrendingContent(20);
      setTrending(response.content);
      if (response.content.length > 0) {
        setSelectedContentId(response.content[0].id);
      }
    } catch (err) {
      setError('Failed to load trending content');
    } finally {
      setLoading(false);
    }
  };

  const loadContentDetails = async (contentId: number) => {
    try {
      setLoading(true);
      const [metricsData, heatmapData, completionData] = await Promise.all([
        getContentMetrics(contentId),
        getContentHeatmap(contentId),
        getCompletionAnalysis(contentId),
      ]);
      setMetrics(metricsData);
      setHeatmap(heatmapData);
      setCompletion(completionData);
    } catch (err) {
      setError('Failed to load content details');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    if (selectedContentId) {
      try {
        const metricsData = await getContentMetrics(selectedContentId, true);
        setMetrics(metricsData);
      } catch (err) {
        setError('Failed to refresh metrics');
      }
    }
  };

  if (loading && !metrics) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl text-gray-400">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Content Analytics</h1>

      {/* Trending Content List */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Trending Content</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {trending.slice(0, 8).map((item) => (
            <div
              key={item.id}
              onClick={() => setSelectedContentId(item.id)}
              className={`p-4 rounded-lg cursor-pointer transition-colors ${
                selectedContentId === item.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 hover:bg-gray-700'
              }`}
            >
              <h3 className="font-medium truncate">{item.title}</h3>
              <div className="flex items-center gap-2 mt-2 text-sm">
                <span className={item.velocity > 1 ? 'text-green-400' : 'text-red-400'}>
                  {item.velocity > 1 ? '^' : 'v'} {item.velocity.toFixed(2)}x
                </span>
                <span className="text-gray-400">Score: {item.trending_score.toFixed(1)}</span>
              </div>
              <div className="text-xs text-gray-400 mt-1">{item.views_24h} views (24h)</div>
            </div>
          ))}
        </div>
      </section>

      {/* Metrics Cards */}
      {metrics && (
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">{metrics.title}</h2>
            <button
              onClick={handleRefresh}
              className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 text-sm"
            >
              Refresh
            </button>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{metrics.total_views.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">Total Views</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{metrics.unique_viewers.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">Unique Viewers</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{metrics.avg_completion_pct.toFixed(1)}%</div>
              <div className="text-gray-400 text-sm">Avg Completion</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{metrics.total_watch_time_hours.toFixed(1)}h</div>
              <div className="text-gray-400 text-sm">Watch Time</div>
            </div>
          </div>
        </section>
      )}

      {/* Engagement Heatmap */}
      {heatmap && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Engagement Heatmap</h2>
          <div className="bg-gray-800 p-4 rounded-lg">
            <EngagementHeatmap heatmapData={heatmap} width={800} height={100} />
          </div>
        </section>
      )}

      {/* Completion Chart */}
      {completion && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Completion Analysis</h2>
          <div className="bg-gray-800 p-4 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">
                  {completion.completion_rate.toFixed(1)}%
                </div>
                <div className="text-gray-400 text-sm">Completion Rate</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">
                  {Math.floor(completion.avg_watch_duration_seconds / 60)} min
                </div>
                <div className="text-gray-400 text-sm">Avg Watch Duration</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{completion.drop_off_points.length}</div>
                <div className="text-gray-400 text-sm">Drop-off Points</div>
              </div>
            </div>
            <CompletionChart completionData={completion} width={800} height={250} />
          </div>
        </section>
      )}
    </div>
  );
}
