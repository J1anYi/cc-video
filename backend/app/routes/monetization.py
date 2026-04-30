"""Monetization routes for creator monetization."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.services.monetization_service import MonetizationService


router = APIRouter(prefix="/creators", tags=["monetization"])


class TipRequest(BaseModel):
    amount: float
    message: Optional[str] = None
    currency: str = "USD"


class PayoutRequest(BaseModel):
    amount: float
    payment_method: str
    payment_details: Optional[dict] = None


class TierCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    benefits: Optional[dict] = None
    billing_period: str = "monthly"
    currency: str = "USD"


class PremiumContentCreate(BaseModel):
    movie_id: int
    title: str
    price: float
    description: Optional[str] = None
    access_type: str = "purchase"
    min_tier: Optional[int] = None
    currency: str = "USD"


@router.get("/{creator_id}/earnings")
async def get_creator_earnings(
    creator_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    if current_user.id != creator_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    service = MonetizationService(db)
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None
    earnings = await service.get_creator_earnings(creator_id, tenant_id, start, end)
    return earnings


@router.post("/{creator_id}/payouts")
async def request_payout(
    creator_id: int,
    data: PayoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    if current_user.id != creator_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    service = MonetizationService(db)
    payout = await service.request_payout(
        creator_id=creator_id, tenant_id=tenant_id, amount=data.amount,
        payment_method=data.payment_method, payment_details=data.payment_details,
    )
    return {"id": payout.id, "amount": payout.amount, "status": payout.status.value}


@router.post("/{creator_id}/tips")
async def send_tip(
    creator_id: int,
    data: TipRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = MonetizationService(db)
    tip = await service.send_tip(
        creator_id=creator_id, sender_id=current_user.id, tenant_id=tenant_id,
        amount=data.amount, message=data.message, currency=data.currency,
    )
    return {"id": tip.id, "amount": tip.amount, "status": tip.status.value}


@router.get("/{creator_id}/tips")
async def get_tips(
    creator_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    if current_user.id != creator_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    service = MonetizationService(db)
    tips = await service.get_tips(creator_id, tenant_id, skip, limit)
    return {"tips": [{"id": t.id, "amount": t.amount, "message": t.message, "created_at": t.created_at.isoformat()} for t in tips]}


@router.post("/{creator_id}/tiers")
async def create_tier(
    creator_id: int,
    data: TierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    if current_user.id != creator_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    service = MonetizationService(db)
    tier = await service.create_creator_tier(
        creator_id=creator_id, tenant_id=tenant_id, name=data.name, price=data.price,
        description=data.description, benefits=data.benefits, billing_period=data.billing_period, currency=data.currency,
    )
    return {"id": tier.id, "name": tier.name, "price": tier.price}


@router.get("/{creator_id}/tiers")
async def get_tiers(creator_id: int, db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    service = MonetizationService(db)
    tiers = await service.get_creator_tiers(creator_id, tenant_id)
    return {"tiers": [{"id": t.id, "name": t.name, "price": t.price, "billing_period": t.billing_period, "subscriber_count": t.subscriber_count} for t in tiers]}


@router.post("/{creator_id}/subscribe")
async def subscribe_to_creator(
    creator_id: int,
    tier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = MonetizationService(db)
    try:
        subscription = await service.subscribe_to_creator(tier_id=tier_id, subscriber_id=current_user.id, tenant_id=tenant_id)
        return {"id": subscription.id, "tier_id": subscription.tier_id, "status": subscription.status.value, "period_end": subscription.current_period_end.isoformat()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/premium-content")
async def create_premium_content(
    data: PremiumContentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = MonetizationService(db)
    content = await service.create_premium_content(
        movie_id=data.movie_id, creator_id=current_user.id, tenant_id=tenant_id,
        title=data.title, price=data.price, description=data.description,
        access_type=data.access_type, min_tier=data.min_tier, currency=data.currency,
    )
    return {"id": content.id, "title": content.title, "price": content.price}


@router.get("/premium-content/{content_id}/access")
async def check_premium_access(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    service = MonetizationService(db)
    has_access = await service.check_premium_access(content_id, current_user.id, tenant_id)
    return {"has_access": has_access}
