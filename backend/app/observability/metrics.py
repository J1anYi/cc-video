from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import asyncio
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class Metric:
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metric_type: str = "gauge"  # gauge, counter, histogram


@dataclass
class HistogramBucket:
    le: float  # less than or equal
    count: int = 0


class MetricsCollector:
    def __init__(self):
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.metrics_history: List[Metric] = []
        self.request_latencies: Dict[str, List[float]] = defaultdict(list)

    def increment_counter(self, name: str, value: float = 1.0, labels: Dict[str, str] = None):
        key = self._make_key(name, labels or {})
        self.counters[key] += value
        self._record_metric(name, self.counters[key], labels or {}, "counter")

    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        key = self._make_key(name, labels or {})
        self.gauges[key] = value
        self._record_metric(name, value, labels or {}, "gauge")

    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        key = self._make_key(name, labels or {})
        self.histograms[key].append(value)
        self._record_metric(name, value, labels or {}, "histogram")

    def record_request_latency(self, endpoint: str, latency_seconds: float, method: str = "GET"):
        labels = {"endpoint": endpoint, "method": method}
        self.request_latencies[endpoint].append(latency_seconds)
        self.observe_histogram("http_request_duration_seconds", latency_seconds, labels)
        self.increment_counter("http_requests_total", labels=labels)

    def record_error(self, error_type: str, endpoint: str):
        labels = {"error_type": error_type, "endpoint": endpoint}
        self.increment_counter("http_errors_total", labels=labels)

    def _make_key(self, name: str, labels: Dict[str, str]) -> str:
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def _record_metric(self, name: str, value: float, labels: Dict[str, str], metric_type: str):
        metric = Metric(
            name=name,
            value=value,
            labels=labels,
            metric_type=metric_type,
        )
        self.metrics_history.append(metric)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                k: {
                    "count": len(v),
                    "sum": sum(v),
                    "avg": sum(v) / len(v) if v else 0,
                    "min": min(v) if v else 0,
                    "max": max(v) if v else 0,
                }
                for k, v in self.histograms.items()
            },
            "history_count": len(self.metrics_history),
        }

    def get_prometheus_format(self) -> str:
        lines = []
        for key, value in self.counters.items():
            lines.append(f"# TYPE {key.split('{')[0]} counter")
            lines.append(f"{key} {value}")
        for key, value in self.gauges.items():
            lines.append(f"# TYPE {key.split('{')[0]} gauge")
            lines.append(f"{key} {value}")
        return "\n".join(lines)

    def get_latency_percentiles(self, endpoint: str = None) -> Dict[str, float]:
        latencies = []
        if endpoint:
            latencies = self.request_latencies.get(endpoint, [])
        else:
            for values in self.request_latencies.values():
                latencies.extend(values)
        
        if not latencies:
            return {"p50": 0, "p90": 0, "p95": 0, "p99": 0}
        
        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)
        return {
            "p50": sorted_latencies[int(n * 0.5)],
            "p90": sorted_latencies[int(n * 0.9)],
            "p95": sorted_latencies[int(n * 0.95)],
            "p99": sorted_latencies[int(n * 0.99)],
        }


# Global metrics collector
metrics = MetricsCollector()
