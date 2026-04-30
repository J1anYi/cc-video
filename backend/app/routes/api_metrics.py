"""API metrics endpoints."""
from fastapi import APIRouter
from app.middleware.response_cache import response_cache
from app.middleware.query_monitor import get_query_monitor

router = APIRouter(prefix="/api-metrics", tags=["api-metrics"])


@router.get("/cache")
async def get_cache_metrics():
    """Get response cache metrics."""
    return response_cache.get_stats()


@router.get("/timing")
async def get_timing_metrics():
    """Get query timing metrics."""
    monitor = get_query_monitor()
    if monitor:
        return monitor.get_stats()
    return {"error": "Query monitor not initialized"}


@router.get("/summary")
async def get_api_summary():
    """Get API performance summary."""
    cache_stats = response_cache.get_stats()
    monitor = get_query_monitor()
    query_stats = monitor.get_stats() if monitor else {}

    return {
        "cache": cache_stats,
        "queries": query_stats,
        "performance": {
            "cache_hit_rate": cache_stats.get("hit_rate", 0),
            "slow_query_count": query_stats.get("slow_query_count", 0),
        }
    }


@router.post("/cache/clear")
async def clear_cache():
    """Clear response cache."""
    response_cache.clear()
    return {"status": "cleared"}
