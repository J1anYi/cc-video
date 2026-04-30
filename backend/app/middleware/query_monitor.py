"""Query performance monitoring middleware."""
import time
import logging
from typing import Callable
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine

logger = logging.getLogger(__name__)


class QueryMonitor:
    """Monitor query performance and log slow queries."""

    def __init__(self, engine: AsyncEngine, slow_query_threshold: float = 0.5):
        self.engine = engine
        self.slow_query_threshold = slow_query_threshold
        self.query_count = 0
        self.slow_queries = []
        self._setup_listeners()

    def _setup_listeners(self):
        """Set up SQLAlchemy event listeners."""
        @event.listens_for(self.engine.sync_engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault("query_start_time", []).append(time.time())
            self.query_count += 1

        @event.listens_for(self.engine.sync_engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total_time = time.time() - conn.info["query_start_time"].pop(-1)
            if total_time > self.slow_query_threshold:
                query_info = {
                    "statement": statement[:500] if len(statement) > 500 else statement,
                    "parameters": str(parameters)[:200] if parameters else None,
                    "duration": total_time,
                    "timestamp": time.time(),
                }
                self.slow_queries.append(query_info)
                logger.warning(
                    f"Slow query detected: {total_time:.3f}s - {statement[:200]}"
                )

    def get_stats(self) -> dict:
        """Get query monitoring statistics."""
        return {
            "total_queries": self.query_count,
            "slow_query_count": len(self.slow_queries),
            "slow_queries": self.slow_queries[-20:],  # Last 20 slow queries
        }

    def reset(self):
        """Reset monitoring stats."""
        self.query_count = 0
        self.slow_queries = []


query_monitor: QueryMonitor | None = None


def init_query_monitor(engine: AsyncEngine, slow_query_threshold: float = 0.5) -> QueryMonitor:
    """Initialize query monitoring for an engine."""
    global query_monitor
    query_monitor = QueryMonitor(engine, slow_query_threshold)
    return query_monitor


def get_query_monitor() -> QueryMonitor | None:
    """Get the global query monitor instance."""
    return query_monitor
