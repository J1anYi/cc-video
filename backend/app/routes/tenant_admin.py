from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db, require_platform_admin, require_admin, get_current_user
from app.models.tenant import Tenant, TenantStatus, TenantPlan
from app.models.user import User, UserRole
from app.services.tenant_service import tenant_service
from app.services.tenant_usage_service import tenant_usage_service


router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=dict)
async def create_tenant(
    name: str,
    slug: str,
    plan: TenantPlan = TenantPlan.BASIC,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    existing = await tenant_service.get_by_slug(db, slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant with this slug already exists",
        )
    tenant = await tenant_service.create(db, name, slug, plan)
    return {
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug,
        "plan": tenant.plan.value,
        "status": tenant.status.value,
    }


@router.get("/", response_model=list)
async def list_tenants(
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> list[dict]:
    tenants = await tenant_service.list_all(db)
    return [
        {
            "id": t.id,
            "name": t.name,
            "slug": t.slug,
            "plan": t.plan.value,
            "status": t.status.value,
            "is_active": t.is_active,
        }
        for t in tenants
    ]


@router.get("/{tenant_id}", response_model=dict)
async def get_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    tenant = await tenant_service.get_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return {
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug,
        "plan": tenant.plan.value,
        "status": tenant.status.value,
        "is_active": tenant.is_active,
        "settings": tenant.settings,
    }


@router.get("/{tenant_id}/stats", response_model=dict)
async def get_tenant_stats(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    return await tenant_usage_service.get_tenant_stats(db, tenant_id)


@router.put("/{tenant_id}", response_model=dict)
async def update_tenant(
    tenant_id: int,
    name: str = None,
    plan: TenantPlan = None,
    status: TenantStatus = None,
    settings: str = None,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    tenant = await tenant_service.update(db, tenant_id, name, plan, status, settings)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return {
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug,
        "plan": tenant.plan.value,
        "status": tenant.status.value,
    }


@router.post("/{tenant_id}/suspend", response_model=dict)
async def suspend_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    tenant = await tenant_service.suspend(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return {"id": tenant.id, "status": tenant.status.value}


@router.post("/{tenant_id}/activate", response_model=dict)
async def activate_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_platform_admin),
) -> dict:
    tenant = await tenant_service.activate(db, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return {"id": tenant.id, "status": tenant.status.value}


@router.get("/{tenant_id}/users", response_model=list)
async def list_tenant_users(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
) -> list[dict]:
    result = await db.execute(select(User).where(User.tenant_id == tenant_id))
    users = result.scalars().all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "display_name": u.display_name,
            "role": u.role.value,
            "is_active": u.is_active,
        }
        for u in users
    ]


@router.post("/{tenant_id}/users/{user_id}/role", response_model=dict)
async def update_user_role(
    tenant_id: int,
    user_id: int,
    role: UserRole,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin),
) -> dict:
    result = await db.execute(select(User).where(User.id == user_id, User.tenant_id == tenant_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role
    await db.commit()
    return {"id": user.id, "role": user.role.value}
