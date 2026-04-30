from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class Span:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    tags: Dict[str, str] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "ok"


@dataclass
class Trace:
    trace_id: str
    spans: List[Span] = field(default_factory=list)
    root_span: Optional[Span] = None
    services: List[str] = field(default_factory=list)


class TraceAggregator:
    def __init__(self):
        self.traces: Dict[str, Trace] = {}
        self.spans: Dict[str, Span] = {}
        self.service_dependencies: Dict[str, List[str]] = defaultdict(list)

    def start_span(
        self,
        trace_id: str,
        span_id: str,
        operation: str,
        parent_span_id: str = None,
        tags: Dict[str, str] = None,
    ) -> Span:
        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            operation=operation,
            start_time=datetime.utcnow(),
            tags=tags or {},
        )
        self.spans[span_id] = span

        if trace_id not in self.traces:
            self.traces[trace_id] = Trace(trace_id=trace_id)
        
        self.traces[trace_id].spans.append(span)
        
        if parent_span_id is None:
            self.traces[trace_id].root_span = span

        return span

    def end_span(self, span_id: str, status: str = "ok"):
        if span_id in self.spans:
            span = self.spans[span_id]
            span.end_time = datetime.utcnow()
            span.duration_ms = (span.end_time - span.start_time).total_seconds() * 1000
            span.status = status

    def add_span_log(self, span_id: str, message: str, **kwargs):
        if span_id in self.spans:
            self.spans[span_id].logs.append({
                "timestamp": datetime.utcnow().isoformat(),
                "message": message,
                **kwargs,
            })

    def record_service_dependency(self, from_service: str, to_service: str):
        if to_service not in self.service_dependencies[from_service]:
            self.service_dependencies[from_service].append(to_service)

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        return self.traces.get(trace_id)

    def get_span(self, span_id: str) -> Optional[Span]:
        return self.spans.get(span_id)

    def get_service_dependencies(self) -> Dict[str, List[str]]:
        return dict(self.service_dependencies)

    def get_trace_statistics(self) -> Dict[str, Any]:
        total_traces = len(self.traces)
        total_spans = len(self.spans)
        
        durations = [
            s.duration_ms for s in self.spans.values()
            if s.duration_ms is not None
        ]
        
        return {
            "total_traces": total_traces,
            "total_spans": total_spans,
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0,
            "max_duration_ms": max(durations) if durations else 0,
            "min_duration_ms": min(durations) if durations else 0,
            "services": list(self.service_dependencies.keys()),
        }

    def cleanup_old_traces(self, max_traces: int = 10000):
        if len(self.traces) > max_traces:
            sorted_traces = sorted(
                self.traces.items(),
                key=lambda x: min(s.start_time for s in x[1].spans) if x[1].spans else datetime.utcnow(),
            )
            for trace_id, _ in sorted_traces[: len(self.traces) - max_traces]:
                del self.traces[trace_id]


# Global trace aggregator
trace_aggregator = TraceAggregator()
