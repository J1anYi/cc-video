from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

class SubscriptionResponse(BaseModel):
    tier: str
    status: str
    billing_cycle: str
    current_period_end: Optional[str]

@router.get("/plans")
async def get_plans():
    return {"plans": [{"id": 1, "key": "free", "name": "Free", "price_monthly": 0, "price_yearly": 0}, {"id": 2, "key": "basic", "name": "Basic", "price_monthly": 9.99, "price_yearly": 99.99}, {"id": 3, "key": "premium", "name": "Premium", "price_monthly": 19.99, "price_yearly": 199.99}]}

@router.get("/current", response_model=SubscriptionResponse)
async def get_current_subscription(current_user: User = Depends(get_current_user)):
    return SubscriptionResponse(tier=current_user.subscription_tier, status=current_user.subscription_status, billing_cycle="monthly", current_period_end=str(current_user.subscription_end) if current_user.subscription_end else None)

@router.post("/upgrade")
async def upgrade_subscription(tier: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.subscription_tier = tier
    current_user.subscription_status = "active"
    await db.commit()
    return {"message": "Upgraded to " + tier}
