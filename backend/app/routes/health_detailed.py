from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any, List

from app.database import engine
from app.observability.metrics import metrics
from app.observability.slo import slo_tracker
from app.observability.tracing import trace_aggregator
import asyncio

router = APIRouter(tags=["health"])


@router.get("/health/detailed")
async def detailed_health():
    """Detailed health check with all components."""
    checks = await run_health_checks()
    overall_status = "healthy" if all(c["status"] == "healthy" for c in checks.values()) else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
    }


async def run_health_checks() -> Dict[str, Any]:
    checks = {}
    
    # Database check
    checks["database"] = await check_database()
    
    # Memory check
    checks["memory"] = check_memory()
    
    # Disk check (simplified)
    checks["disk"] = check_disk()
    
    # API response time
    checks["api_latency"] = check_api_latency()
    
    return checks


async def check_database() -> Dict[str, Any]:
    try:
        start = datetime.utcnow()
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        latency = (datetime.utcnow() - start).total_seconds() * 1000
        return {
            "status": "healthy",
            "latency_ms": round(latency, 2),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }


def check_memory() -> Dict[str, Any]:
    try:
        import psutil
        memory = psutil.virtual_memory()
        return {
            "status": "healthy" if memory.percent < 90 else "warning",
            "used_percent": memory.percent,
            "available_mb": memory.available // (1024 * 1024),
        }
    except ImportError:
        return {"status": "unknown", "message": "psutil not installed"}


def check_disk() -> Dict[str, Any]:
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        used_percent = (used / total) * 100
        return {
            "status": "healthy" if used_percent < 90 else "warning",
            "used_percent": round(used_percent, 2),
            "free_gb": free // (1024 * 1024 * 1024),
        }
    except Exception:
        return {"status": "unknown"}


def check_api_latency() -> Dict[str, Any]:
    percentiles = metrics.get_latency_percentiles()
    return {
        "status": "healthy" if percentiles["p99"] < 500 else "warning",
        "p50": round(percentiles["p50"] * 1000, 2),
        "p90": round(percentiles["p90"] * 1000, 2),
        "p95": round(percentiles["p95"] * 1000, 2),
        "p99": round(percentiles["p99"] * 1000, 2),
    }


@router.get("/metrics")
async def get_metrics():
    """Get current metrics."""
    return metrics.get_metrics()


@router.get("/metrics/prometheus")
async def get_prometheus_metrics():
    """Get metrics in Prometheus format."""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(content=metrics.get_prometheus_format())


@router.get("/metrics/latency")
async def get_latency_metrics():
    """Get latency percentiles."""
    return metrics.get_latency_percentiles()


@router.get("/slo")
async def get_slo_status():
    """Get SLO status and error budget."""
    return slo_tracker.get_error_budget_report()


@router.get("/slo/{slo_name}")
async def get_slo_detail(slo_name: str):
    """Get specific SLO details."""
    status = slo_tracker.get_slo_status(slo_name)
    if not status:
        return {"error": f"SLO {slo_name} not found"}
    return {
        "name": status.slo_name,
        "current": status.current_value,
        "target": status.target,
        "budget_remaining": status.error_budget_remaining,
        "budget_consumed": status.error_budget_consumed,
        "burn_rate": status.burn_rate,
        "status": status.status,
    }


@router.get("/traces/stats")
async def get_trace_stats():
    """Get trace statistics."""
    return trace_aggregator.get_trace_statistics()


@router.get("/traces/dependencies")
async def get_service_dependencies():
    """Get service dependency graph."""
    return {
        "dependencies": trace_aggregator.get_service_dependencies(),
    }


@router.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    """Get trace by ID."""
    trace = trace_aggregator.get_trace(trace_id)
    if not trace:
        return {"error": f"Trace {trace_id} not found"}
    return {
        "trace_id": trace.trace_id,
        "spans": [
            {
                "span_id": s.span_id,
                "parent_span_id": s.parent_span_id,
                "operation": s.operation,
                "duration_ms": s.duration_ms,
                "status": s.status,
                "tags": s.tags,
            }
            for s in trace.spans
        ],
    }
