from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.models.movie import Movie


class TenantUsageService:
    async def get_tenant_stats(self, db: AsyncSession, tenant_id: int) -> dict:
        users_count = await self._count_users(db, tenant_id)
        movies_count = await self._count_movies(db, tenant_id)
        storage_used = await self._calculate_storage(db, tenant_id)
        
        return {
            "tenant_id": tenant_id,
            "users_count": users_count,
            "movies_count": movies_count,
            "storage_bytes": storage_used,
            "storage_gb": round(storage_used / (1024**3), 2),
        }

    async def _count_users(self, db: AsyncSession, tenant_id: int) -> int:
        result = await db.execute(
            select(func.count()).where(User.tenant_id == tenant_id)
        )
        return result.scalar() or 0

    async def _count_movies(self, db: AsyncSession, tenant_id: int) -> int:
        result = await db.execute(
            select(func.count()).where(Movie.tenant_id == tenant_id)
        )
        return result.scalar() or 0

    async def _calculate_storage(self, db: AsyncSession, tenant_id: int) -> int:
        from app.models.video_file import VideoFile
        
        result = await db.execute(
            select(func.sum(VideoFile.file_size))
            .join(Movie, VideoFile.movie_id == Movie.id)
            .where(Movie.tenant_id == tenant_id)
        )
        return result.scalar() or 0


tenant_usage_service = TenantUsageService()
