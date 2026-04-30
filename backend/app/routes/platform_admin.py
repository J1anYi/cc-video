from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.dependencies import get_db, require_platform_admin
from app.models.tenant import Tenant
from app.models.user import User
from app.models.movie import Movie
from app.services.tenant_service import tenant_service


router = APIRouter(prefix="/platform", tags=["platform"])


@router.get("/stats", response_model=dict)
async def get_platform_stats(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    tenants_count = await db.execute(select(func.count()).select_from(Tenant))
    users_count = await db.execute(select(func.count()).select_from(User))
    movies_count = await db.execute(select(func.count()).select_from(Movie))
    
    return {
        "tenants_count": tenants_count.scalar() or 0,
        "users_count": users_count.scalar() or 0,
        "movies_count": movies_count.scalar() or 0,
    }


@router.get("/tenants", response_model=list)
async def get_all_tenants_stats(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> list[dict]:
    from app.services.tenant_usage_service import tenant_usage_service
    
    tenants = await tenant_service.list_all(db)
    result = []
    for t in tenants:
        stats = await tenant_usage_service.get_tenant_stats(db, t.id)
        result.append({
            "id": t.id,
            "name": t.name,
            "slug": t.slug,
            "plan": t.plan.value,
            "status": t.status.value,
            "users_count": stats["users_count"],
            "movies_count": stats["movies_count"],
            "storage_gb": stats["storage_gb"],
        })
    return result


@router.get("/health", response_model=dict)
async def get_platform_health(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    try:
        await db.execute(select(1))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
    }
