"""Database configuration with connection pooling, read replicas, and monitoring."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Primary engine for writes
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_pre_ping=True,
)

# Read replica engine (optional - same as primary if not configured)
read_replica_url = getattr(settings, 'DATABASE_READ_REPLICA_URL', None)
if read_replica_url:
    read_engine = create_async_engine(
        read_replica_url,
        echo=settings.DEBUG,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        pool_recycle=settings.DATABASE_POOL_RECYCLE,
        pool_pre_ping=True,
    )
    logger.info(f"Read replica configured: {read_replica_url}")
else:
    read_engine = engine  # Fall back to primary

# Session factories
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

ReadSessionLocal = async_sessionmaker(
    read_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Get database session for writes."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_read_db():
    """Get database session for reads (uses replica if configured)."""
    async with ReadSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
