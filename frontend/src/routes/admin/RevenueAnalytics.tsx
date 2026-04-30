import { useState, useEffect } from 'react';
import { getSubscriptionMetrics, getArpu, getLtv, getPaymentFailures, getRevenueForecast } from '../../api/revenue';

export default function RevenueAnalytics() {
  const [metrics, setMetrics] = useState<any>(null);
  const [arpu, setArpu] = useState<any>(null);
  const [ltv, setLtv] = useState<any>(null);
  const [failures, setFailures] = useState<any>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    try {
      setLoading(true);
      const [m, a, l, f, fc] = await Promise.all([
        getSubscriptionMetrics(),
        getArpu(),
        getLtv(),
        getPaymentFailures(),
        getRevenueForecast(),
      ]);
      setMetrics(m);
      setArpu(a);
      setLtv(l);
      setFailures(f);
      setForecast(fc);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-gray-400">Loading revenue analytics...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Revenue Analytics</h1>

      {metrics && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Subscription Metrics</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">${metrics.mrr.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">MRR</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">${metrics.arr.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">ARR</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{(metrics.growth_rate * 100).toFixed(1)}%</div>
              <div className="text-gray-400 text-sm">Growth Rate</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{(metrics.churn_rate * 100).toFixed(1)}%</div>
              <div className="text-gray-400 text-sm">Churn Rate</div>
            </div>
          </div>
        </section>
      )}

      {arpu && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">ARPU</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">${arpu.overall_arpu.toFixed(2)}</div>
              <div className="text-gray-400 text-sm">Overall ARPU</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{arpu.paying_users}</div>
              <div className="text-gray-400 text-sm">Paying Users</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{arpu.total_users}</div>
              <div className="text-gray-400 text-sm">Total Users</div>
            </div>
          </div>
        </section>
      )}

      {ltv && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Lifetime Value</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">${ltv.overall_ltv.toFixed(2)}</div>
              <div className="text-gray-400 text-sm">Average LTV</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">{ltv.avg_subscription_months.toFixed(1)}</div>
              <div className="text-gray-400 text-sm">Avg Months</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-3xl font-bold">${ltv.total_lifetime_revenue.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">Total Revenue</div>
            </div>
          </div>
        </section>
      )}

      {forecast && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Revenue Forecast</h2>
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-xl font-bold">${forecast.current_mrr.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">Current MRR</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-xl font-bold">${forecast.projected_mrr_3m.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">3 Months</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-xl font-bold">${forecast.projected_mrr_6m.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">6 Months</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-xl font-bold">${forecast.projected_mrr_12m.toLocaleString()}</div>
              <div className="text-gray-400 text-sm">12 Months</div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
