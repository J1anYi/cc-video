from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tenant import Tenant, TenantStatus, TenantPlan


class TenantService:
    async def get_by_id(self, db: AsyncSession, tenant_id: int) -> Optional[Tenant]:
        result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Tenant]:
        result = await db.execute(select(Tenant).where(Tenant.slug == slug))
        return result.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        name: str,
        slug: str,
        plan: TenantPlan = TenantPlan.BASIC,
        status: TenantStatus = TenantStatus.ACTIVE
    ) -> Tenant:
        tenant = Tenant(name=name, slug=slug, plan=plan, status=status)
        db.add(tenant)
        await db.commit()
        await db.refresh(tenant)
        return tenant

    async def update(
        self,
        db: AsyncSession,
        tenant_id: int,
        name: Optional[str] = None,
        plan: Optional[TenantPlan] = None,
        status: Optional[TenantStatus] = None,
        settings: Optional[str] = None
    ) -> Optional[Tenant]:
        tenant = await self.get_by_id(db, tenant_id)
        if not tenant:
            return None
        if name:
            tenant.name = name
        if plan:
            tenant.plan = plan
        if status:
            tenant.status = status
        if settings is not None:
            tenant.settings = settings
        await db.commit()
        await db.refresh(tenant)
        return tenant

    async def suspend(self, db: AsyncSession, tenant_id: int) -> Optional[Tenant]:
        return await self.update(db, tenant_id, status=TenantStatus.SUSPENDED)

    async def activate(self, db: AsyncSession, tenant_id: int) -> Optional[Tenant]:
        return await self.update(db, tenant_id, status=TenantStatus.ACTIVE)

    async def list_all(self, db: AsyncSession) -> list[Tenant]:
        result = await db.execute(select(Tenant).order_by(Tenant.created_at.desc()))
        return list(result.scalars().all())


tenant_service = TenantService()
