import json
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.tenant import Tenant
from app.schemas.branding import BrandingSettings, BrandingUpdate


class BrandingService:
    async def get_branding(self, db: AsyncSession, tenant_id: int) -> BrandingSettings:
        result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
        tenant = result.scalar_one_or_none()
        
        if not tenant or not tenant.settings:
            return BrandingSettings()
        
        settings_dict = json.loads(tenant.settings)
        return BrandingSettings(**settings_dict)

    async def update_branding(
        self,
        db: AsyncSession,
        tenant_id: int,
        update: BrandingUpdate
    ) -> BrandingSettings:
        result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
        tenant = result.scalar_one_or_none()
        
        if not tenant:
            raise ValueError("Tenant not found")
        
        current = await self.get_branding(db, tenant_id)
        
        update_data = update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(current, key, value)
        
        tenant.settings = json.dumps(current.model_dump())
        await db.commit()
        await db.refresh(tenant)
        
        return current

    async def set_logo(
        self,
        db: AsyncSession,
        tenant_id: int,
        logo_url: str
    ) -> BrandingSettings:
        return await self.update_branding(db, tenant_id, BrandingUpdate(logo_url=logo_url))

    async def set_favicon(
        self,
        db: AsyncSession,
        tenant_id: int,
        favicon_url: str
    ) -> BrandingSettings:
        return await self.update_branding(db, tenant_id, BrandingUpdate(favicon_url=favicon_url))


branding_service = BrandingService()
