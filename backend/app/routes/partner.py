"""Partner API routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import secrets

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.models.partner import Partner, PartnerAPIKey, PartnerRevenue

router = APIRouter(prefix="/partners", tags=["partners"])

class PartnerCreate(BaseModel):
    name: str
    contact_email: str
    revenue_share_percent: float = 0.0

class APIKeyCreate(BaseModel):
    key_name: str

@router.post("")
async def create_partner(data: PartnerCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    api_key = secrets.token_urlsafe(32)
    partner = Partner(tenant_id=tenant_id, name=data.name, contact_email=data.contact_email, api_key=api_key, revenue_share_percent=data.revenue_share_percent)
    db.add(partner)
    await db.commit()
    return {"id": partner.id, "name": partner.name, "api_key": api_key}

@router.get("")
async def get_partners(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    from sqlalchemy import select
    query = select(Partner).where(Partner.tenant_id == tenant_id, Partner.is_active == True)
    result = await db.execute(query)
    partners = result.scalars().all()
    return {"partners": [{"id": p.id, "name": p.name, "contact_email": p.contact_email} for p in partners]}

@router.post("/{partner_id}/keys")
async def create_api_key(partner_id: int, data: APIKeyCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    key = secrets.token_urlsafe(32)
    api_key = PartnerAPIKey(partner_id=partner_id, key_name=data.key_name, api_key=key)
    db.add(api_key)
    await db.commit()
    return {"id": api_key.id, "key_name": api_key.key_name, "api_key": key}

@router.get("/{partner_id}/revenue")
async def get_partner_revenue(partner_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    from sqlalchemy import select, func
    query = select(func.sum(PartnerRevenue.partner_share)).where(PartnerRevenue.partner_id == partner_id, PartnerRevenue.tenant_id == tenant_id)
    result = await db.execute(query)
    total = result.scalar() or 0
    return {"partner_id": partner_id, "total_revenue": total}
