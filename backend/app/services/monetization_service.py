"""Monetization service for creator monetization operations."""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.monetization import (
    CreatorEarnings,
    Payout,
    Tip,
    PremiumContent,
    CreatorTier,
    CreatorSubscription,
    PayoutStatus,
    TipStatus,
    SubscriptionStatus,
)


class MonetizationService:
    """Service for creator monetization operations."""

    PLATFORM_FEE_PERCENT = 0.10  # 10% platform fee

    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_earnings(
        self,
        creator_id: int,
        tenant_id: int,
        source_type: str,
        gross_amount: float,
        source_id: Optional[int] = None,
        currency: str = "USD",
    ) -> CreatorEarnings:
        """Record earnings for a creator."""
        platform_fee = gross_amount * self.PLATFORM_FEE_PERCENT
        net_amount = gross_amount - platform_fee

        earnings = CreatorEarnings(
            creator_id=creator_id,
            tenant_id=tenant_id,
            source_type=source_type,
            source_id=source_id,
            gross_amount=gross_amount,
            platform_fee=platform_fee,
            net_amount=net_amount,
            currency=currency,
        )
        self.db.add(earnings)
        await self.db.commit()
        await self.db.refresh(earnings)
        return earnings

    async def get_creator_earnings(
        self,
        creator_id: int,
        tenant_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get earnings summary for a creator."""
        query = select(CreatorEarnings).where(
            CreatorEarnings.creator_id == creator_id,
            CreatorEarnings.tenant_id == tenant_id,
        )

        if start_date:
            query = query.where(CreatorEarnings.created_at >= start_date)
        if end_date:
            query = query.where(CreatorEarnings.created_at <= end_date)

        result = await self.db.execute(query)
        earnings = result.scalars().all()

        total_gross = sum(e.gross_amount for e in earnings)
        total_fees = sum(e.platform_fee for e in earnings)
        total_net = sum(e.net_amount for e in earnings)

        # Get available balance
        available_query = select(func.sum(CreatorEarnings.net_amount)).where(
            CreatorEarnings.creator_id == creator_id,
            CreatorEarnings.tenant_id == tenant_id,
            CreatorEarnings.status == "available",
        )
        available_result = await self.db.execute(available_query)
        available_balance = available_result.scalar() or 0

        return {
            "total_gross": total_gross,
            "total_fees": total_fees,
            "total_net": total_net,
            "available_balance": available_balance,
            "earnings_count": len(earnings),
        }

    async def request_payout(
        self,
        creator_id: int,
        tenant_id: int,
        amount: float,
        payment_method: str,
        payment_details: Optional[dict] = None,
    ) -> Payout:
        """Request a payout."""
        payout = Payout(
            creator_id=creator_id,
            tenant_id=tenant_id,
            amount=amount,
            payment_method=payment_method,
            payment_details=payment_details,
        )
        self.db.add(payout)
        await self.db.commit()
        await self.db.refresh(payout)
        return payout

    async def process_payout(
        self,
        payout_id: int,
        transaction_id: str,
        success: bool = True,
    ) -> Optional[Payout]:
        """Process a payout."""
        payout = await self.db.get(Payout, payout_id)
        if not payout:
            return None

        payout.transaction_id = transaction_id
        payout.processed_at = datetime.utcnow()
        payout.status = PayoutStatus.COMPLETED if success else PayoutStatus.FAILED

        await self.db.commit()
        await self.db.refresh(payout)
        return payout

    async def send_tip(
        self,
        creator_id: int,
        sender_id: int,
        tenant_id: int,
        amount: float,
        message: Optional[str] = None,
        currency: str = "USD",
    ) -> Tip:
        """Send a tip to a creator."""
        platform_fee = amount * self.PLATFORM_FEE_PERCENT
        net_amount = amount - platform_fee

        tip = Tip(
            creator_id=creator_id,
            sender_id=sender_id,
            tenant_id=tenant_id,
            amount=amount,
            platform_fee=platform_fee,
            net_amount=net_amount,
            message=message,
            currency=currency,
            status=TipStatus.COMPLETED,
        )
        self.db.add(tip)

        # Record earnings for creator
        await self.record_earnings(
            creator_id=creator_id,
            tenant_id=tenant_id,
            source_type="tip",
            gross_amount=amount,
            source_id=tip.id,
            currency=currency,
        )

        await self.db.commit()
        await self.db.refresh(tip)
        return tip

    async def get_tips(
        self,
        creator_id: int,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Tip]:
        """Get tips received by a creator."""
        query = select(Tip).where(
            Tip.creator_id == creator_id,
            Tip.tenant_id == tenant_id,
            Tip.status == TipStatus.COMPLETED,
        ).order_by(Tip.created_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_premium_content(
        self,
        movie_id: int,
        creator_id: int,
        tenant_id: int,
        title: str,
        price: float,
        description: Optional[str] = None,
        access_type: str = "purchase",
        min_tier: Optional[int] = None,
        currency: str = "USD",
    ) -> PremiumContent:
        """Create premium gated content."""
        content = PremiumContent(
            movie_id=movie_id,
            creator_id=creator_id,
            tenant_id=tenant_id,
            title=title,
            description=description,
            price=price,
            currency=currency,
            access_type=access_type,
            min_tier=min_tier,
        )
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content

    async def check_premium_access(
        self,
        content_id: int,
        user_id: int,
        tenant_id: int,
    ) -> bool:
        """Check if user has access to premium content."""
        content = await self.db.get(PremiumContent, content_id)
        if not content or not content.is_active:
            return False

        if content.access_type == "purchase":
            # Check if user purchased
            from app.models.marketplace import License
            query = select(License).where(
                License.listing_id == content_id,
                License.buyer_id == user_id,
                License.status == "active",
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none() is not None

        elif content.access_type == "subscription":
            # Check if user has active subscription
            query = select(CreatorSubscription).where(
                CreatorSubscription.subscriber_id == user_id,
                CreatorSubscription.tenant_id == tenant_id,
                CreatorSubscription.status == SubscriptionStatus.ACTIVE,
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none() is not None

        elif content.access_type == "tier" and content.min_tier:
            # Check if user has required tier subscription
            query = select(CreatorSubscription).where(
                CreatorSubscription.subscriber_id == user_id,
                CreatorSubscription.tenant_id == tenant_id,
                CreatorSubscription.status == SubscriptionStatus.ACTIVE,
                CreatorSubscription.tier_id >= content.min_tier,
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none() is not None

        return False

    async def create_creator_tier(
        self,
        creator_id: int,
        tenant_id: int,
        name: str,
        price: float,
        description: Optional[str] = None,
        benefits: Optional[dict] = None,
        billing_period: str = "monthly",
        currency: str = "USD",
    ) -> CreatorTier:
        """Create a subscription tier for a creator."""
        tier = CreatorTier(
            creator_id=creator_id,
            tenant_id=tenant_id,
            name=name,
            description=description,
            price=price,
            currency=currency,
            billing_period=billing_period,
            benefits=benefits,
        )
        self.db.add(tier)
        await self.db.commit()
        await self.db.refresh(tier)
        return tier

    async def get_creator_tiers(
        self,
        creator_id: int,
        tenant_id: int,
    ) -> List[CreatorTier]:
        """Get all tiers for a creator."""
        query = select(CreatorTier).where(
            CreatorTier.creator_id == creator_id,
            CreatorTier.tenant_id == tenant_id,
            CreatorTier.is_active == True,
        ).order_by(CreatorTier.price.asc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def subscribe_to_creator(
        self,
        tier_id: int,
        subscriber_id: int,
        tenant_id: int,
    ) -> CreatorSubscription:
        """Subscribe to a creator's tier."""
        tier = await self.db.get(CreatorTier, tier_id)
        if not tier or not tier.is_active:
            raise ValueError("Tier not found or inactive")

        # Calculate period end
        if tier.billing_period == "monthly":
            period_end = datetime.utcnow() + timedelta(days=30)
        elif tier.billing_period == "yearly":
            period_end = datetime.utcnow() + timedelta(days=365)
        else:
            period_end = datetime.utcnow() + timedelta(days=30)

        subscription = CreatorSubscription(
            tier_id=tier_id,
            subscriber_id=subscriber_id,
            tenant_id=tenant_id,
            current_period_end=period_end,
        )
        self.db.add(subscription)

        # Update tier subscriber count
        tier.subscriber_count += 1

        # Record earnings for creator
        await self.record_earnings(
            creator_id=tier.creator_id,
            tenant_id=tenant_id,
            source_type="subscription",
            gross_amount=tier.price,
            source_id=subscription.id,
            currency=tier.currency,
        )

        await self.db.commit()
        await self.db.refresh(subscription)
        return subscription

    async def get_creator_subscribers(
        self,
        creator_id: int,
        tenant_id: int,
    ) -> List[CreatorSubscription]:
        """Get subscribers for a creator."""
        query = select(CreatorSubscription).join(CreatorTier).where(
            CreatorTier.creator_id == creator_id,
            CreatorSubscription.tenant_id == tenant_id,
            CreatorSubscription.status == SubscriptionStatus.ACTIVE,
        ).options(selectinload(CreatorSubscription.tier))

        result = await self.db.execute(query)
        return result.scalars().all()
