"""Phase 198: Creator Monetization Routes"""
from fastapi import APIRouter
from ..services.creator_monetization import CreatorMonetizationService

router = APIRouter(prefix="/api/creator-monetization", tags=["creator-monetization"])
service = CreatorMonetizationService()

@router.post("/subscription/{creator_id}")
async def create_tier(creator_id: str, tier_data: dict):
    return await service.create_subscription_tier(creator_id, tier_data)

@router.post("/ad-revenue/{creator_id}")
async def config_ads(creator_id: str, ad_config: dict):
    return await service.configure_ad_revenue(creator_id, ad_config)

@router.post("/tip-jar/{creator_id}")
async def setup_tips(creator_id: str):
    return await service.setup_tip_jar(creator_id)

@router.post("/merchandise/{creator_id}")
async def integrate_merch(creator_id: str, products: list):
    return await service.integrate_merchandise(creator_id, products)

@router.post("/premium-gating/{content_id}")
async def setup_gate(content_id: str, gate_config: dict):
    return await service.setup_premium_gating(content_id, gate_config)
