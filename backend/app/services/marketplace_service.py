"""Marketplace service for content marketplace operations."""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.marketplace import (
    MarketplaceListing,
    PricingTier,
    License,
    ContentPreview,
    MarketplaceReview,
    PricingType,
    ListingStatus,
    LicenseStatus,
    PreviewType,
)


class MarketplaceService:
    """Service for marketplace operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_listing(
        self,
        movie_id: int,
        seller_id: int,
        tenant_id: int,
        title: str,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        pricing_type: PricingType = PricingType.PURCHASE,
        base_price: float = 0.0,
        currency: str = "USD",
    ) -> MarketplaceListing:
        """Create a new marketplace listing."""
        listing = MarketplaceListing(
            movie_id=movie_id,
            seller_id=seller_id,
            tenant_id=tenant_id,
            title=title,
            description=description,
            tags=tags,
            pricing_type=pricing_type,
            base_price=base_price,
            currency=currency,
        )
        self.db.add(listing)
        await self.db.commit()
        await self.db.refresh(listing)
        return listing

    async def get_listings(
        self,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        pricing_type: Optional[PricingType] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        seller_id: Optional[int] = None,
    ) -> List[MarketplaceListing]:
        """Get marketplace listings with filters."""
        query = select(MarketplaceListing).where(
            MarketplaceListing.tenant_id == tenant_id,
            MarketplaceListing.status == ListingStatus.ACTIVE,
        ).options(selectinload(MarketplaceListing.pricing_tiers))

        if search:
            query = query.where(
                or_(
                    MarketplaceListing.title.ilike(f"%{search}%"),
                    MarketplaceListing.description.ilike(f"%{search}%"),
                    MarketplaceListing.tags.ilike(f"%{search}%"),
                )
            )

        if pricing_type:
            query = query.where(MarketplaceListing.pricing_type == pricing_type)

        if min_price is not None:
            query = query.where(MarketplaceListing.base_price >= min_price)

        if max_price is not None:
            query = query.where(MarketplaceListing.base_price <= max_price)

        if seller_id:
            query = query.where(MarketplaceListing.seller_id == seller_id)

        query = query.order_by(MarketplaceListing.created_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_listing_by_id(self, listing_id: int, tenant_id: int) -> Optional[MarketplaceListing]:
        """Get a listing by ID."""
        query = select(MarketplaceListing).where(
            MarketplaceListing.id == listing_id,
            MarketplaceListing.tenant_id == tenant_id,
        ).options(
            selectinload(MarketplaceListing.pricing_tiers),
            selectinload(MarketplaceListing.previews),
            selectinload(MarketplaceListing.reviews),
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_listing(
        self,
        listing_id: int,
        tenant_id: int,
        seller_id: int,
        **kwargs,
    ) -> Optional[MarketplaceListing]:
        """Update a listing (only by owner)."""
        listing = await self.get_listing_by_id(listing_id, tenant_id)
        if not listing or listing.seller_id != seller_id:
            return None

        for key, value in kwargs.items():
            if hasattr(listing, key) and value is not None:
                setattr(listing, key, value)

        await self.db.commit()
        await self.db.refresh(listing)
        return listing

    async def delete_listing(self, listing_id: int, tenant_id: int, seller_id: int) -> bool:
        """Delete a listing (only by owner)."""
        listing = await self.get_listing_by_id(listing_id, tenant_id)
        if not listing or listing.seller_id != seller_id:
            return False

        await self.db.delete(listing)
        await self.db.commit()
        return True

    async def add_pricing_tier(
        self,
        listing_id: int,
        name: str,
        price: float,
        duration_days: Optional[int] = None,
        features: Optional[dict] = None,
    ) -> PricingTier:
        """Add a pricing tier to a listing."""
        tier = PricingTier(
            listing_id=listing_id,
            name=name,
            price=price,
            duration_days=duration_days,
            features=features,
        )
        self.db.add(tier)
        await self.db.commit()
        await self.db.refresh(tier)
        return tier

    async def purchase_license(
        self,
        listing_id: int,
        buyer_id: int,
        tenant_id: int,
        tier_id: Optional[int] = None,
        transaction_id: Optional[str] = None,
    ) -> License:
        """Purchase a license for a listing."""
        listing = await self.get_listing_by_id(listing_id, tenant_id)
        if not listing:
            raise ValueError("Listing not found")

        # Determine price
        price_paid = listing.base_price
        license_type = listing.pricing_type.value
        valid_until = None

        if tier_id:
            tier = await self.db.get(PricingTier, tier_id)
            if tier and tier.listing_id == listing_id:
                price_paid = tier.price
                if tier.duration_days:
                    valid_until = datetime.utcnow() + timedelta(days=tier.duration_days)

        # Create license
        license_obj = License(
            listing_id=listing_id,
            buyer_id=buyer_id,
            tenant_id=tenant_id,
            license_type=license_type,
            price_paid=price_paid,
            currency=listing.currency,
            valid_until=valid_until,
            transaction_id=transaction_id,
        )
        self.db.add(license_obj)

        # Update purchase count
        listing.purchase_count += 1

        await self.db.commit()
        await self.db.refresh(license_obj)
        return license_obj

    async def get_user_licenses(self, user_id: int, tenant_id: int) -> List[License]:
        """Get all licenses for a user."""
        query = select(License).where(
            License.buyer_id == user_id,
            License.tenant_id == tenant_id,
            License.status == LicenseStatus.ACTIVE,
        ).options(selectinload(License.listing)).order_by(License.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def add_preview(
        self,
        listing_id: int,
        preview_type: PreviewType,
        video_url: str,
        thumbnail_url: Optional[str] = None,
        duration_seconds: int = 0,
    ) -> ContentPreview:
        """Add a preview to a listing."""
        preview = ContentPreview(
            listing_id=listing_id,
            preview_type=preview_type,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            duration_seconds=duration_seconds,
        )
        self.db.add(preview)
        await self.db.commit()
        await self.db.refresh(preview)
        return preview

    async def add_review(
        self,
        listing_id: int,
        user_id: int,
        tenant_id: int,
        rating: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ) -> MarketplaceReview:
        """Add a review to a listing."""
        review = MarketplaceReview(
            listing_id=listing_id,
            user_id=user_id,
            tenant_id=tenant_id,
            rating=rating,
            title=title,
            content=content,
        )
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def get_reviews(
        self,
        listing_id: int,
        tenant_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> List[MarketplaceReview]:
        """Get reviews for a listing."""
        query = select(MarketplaceReview).where(
            MarketplaceReview.listing_id == listing_id,
            MarketplaceReview.tenant_id == tenant_id,
        ).order_by(MarketplaceReview.helpful_count.desc(), MarketplaceReview.created_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_listing_stats(self, listing_id: int, tenant_id: int) -> Dict[str, Any]:
        """Get statistics for a listing."""
        listing = await self.get_listing_by_id(listing_id, tenant_id)
        if not listing:
            return {}

        # Calculate average rating
        avg_rating_query = select(func.avg(MarketplaceReview.rating)).where(
            MarketplaceReview.listing_id == listing_id,
        )
        avg_result = await self.db.execute(avg_rating_query)
        avg_rating = avg_result.scalar() or 0

        # Count reviews
        count_query = select(func.count(MarketplaceReview.id)).where(
            MarketplaceReview.listing_id == listing_id,
        )
        count_result = await self.db.execute(count_query)
        review_count = count_result.scalar() or 0

        return {
            "view_count": listing.view_count,
            "purchase_count": listing.purchase_count,
            "review_count": review_count,
            "avg_rating": round(float(avg_rating), 2),
        }
