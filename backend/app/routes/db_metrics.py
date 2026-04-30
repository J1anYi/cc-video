"""Database metrics routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database import get_db, engine
from app.middleware.query_monitor import get_query_monitor


router = APIRouter(prefix="/db", tags=["database"])


@router.get("/stats")
async def get_db_stats():
    """Get database statistics."""
    monitor = get_query_monitor()
    stats = {
        "pool_size": engine.pool.size() if hasattr(engine, 'pool') else 0,
        "checked_in": engine.pool.checkedin() if hasattr(engine, 'pool') else 0,
        "checked_out": engine.pool.checkedout() if hasattr(engine, 'pool') else 0,
        "overflow": engine.pool.overflow() if hasattr(engine, 'pool') else 0,
    }
    if monitor:
        stats["queries"] = monitor.get_stats()
    return stats


@router.get("/health")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """Check database connectivity and response time."""
    import time
    start = time.time()
    await db.execute(text("SELECT 1"))
    latency = time.time() - start
    return {
        "status": "healthy",
        "latency_ms": round(latency * 1000, 2),
    }


@router.get("/indexes")
async def get_db_indexes(db: AsyncSession = Depends(get_db)):
    """List database indexes."""
    # SQLite query to get indexes
    result = await db.execute(text(
        "SELECT name, tbl_name FROM sqlite_master WHERE type='index' ORDER BY tbl_name, name"
    ))
    indexes = [{"name": row[0], "table": row[1]} for row in result.fetchall()]
    return {"indexes": indexes}


@router.post("/analyze")
async def analyze_tables(db: AsyncSession = Depends(get_db)):
    """Analyze tables for query optimization."""
    # Get list of tables
    result = await db.execute(text(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ))
    tables = [row[0] for row in result.fetchall()]

    # Analyze each table
    for table in tables:
        await db.execute(text(f"ANALYZE {table}"))
    await db.commit()

    return {"analyzed_tables": tables}
