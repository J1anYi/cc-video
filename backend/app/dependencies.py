from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Placeholder - will be implemented in Wave 2
async def get_current_user():
    """Dependency to get current user from JWT token. Implemented in Wave 2."""
    pass
