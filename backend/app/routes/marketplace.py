"""Marketplace routes for content marketplace."""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user, get_current_user_optional
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.services.marketplace_service import MarketplaceService
from app.models.marketplace import PricingType, PreviewType


router = APIRouter(prefix="/marketplace", tags=["marketplace"])


# Pydantic schemas
class ListingCreate(BaseModel):
    movie_id: int
    title: str
    description: Optional[str] = None
    tags: Optional[str] = None
    pricing_type: str = "purchase"
    base_price: float = 0.0
    currency: str = "USD"


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    pricing_type: Optional[str] = None
    base_price: Optional[float] = None
    status: Optional[str] = None


class PricingTierCreate(BaseModel):
    name: str
    price: float
    duration_days: Optional[int] = None
    features: Optional[dict] = None


class PurchaseRequest(BaseModel):
    tier_id: Optional[int] = None
    transaction_id: Optional[str] = None


class ReviewCreate(BaseModel):
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None


class PreviewCreate(BaseModel):
    preview_type: str
    video_url: str
    thumbnail_url: Optional[str] = None
    duration_seconds: int = 0


class ListingResponse(BaseModel):
    id: int
    movie_id: int
    seller_id: int
    title: str
    description: Optional[str]
    tags: Optional[str]
    pricing_type: str
    base_price: float
    currency: str
    status: str
    view_count: int
    purchase_count: int
    created_at: str

    class Config:
        from_attributes = True


class LicenseResponse(BaseModel):
    id: int
    listing_id: int
    license_type: str
    price_paid: float
    currency: str
    valid_from: str
    valid_until: Optional[str]
    status: str

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    id: int
    listing_id: int
    user_id: int
    rating: int
    title: Optional[str]
    content: Optional[str]
    helpful_count: int
    created_at: str

    class Config:
        from_attributes = True


@router.get("")
async def get_listings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    pricing_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    seller_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Browse marketplace listings."""
    service = MarketplaceService(db)

    pricing_enum = None
    if pricing_type:
        try:
            pricing_enum = PricingType(pricing_type)
        except ValueError:
            pass

    listings = await service.get_listings(
        tenant_id=tenant_id,
        skip=skip,
        limit=limit,
        search=search,
        pricing_type=pricing_enum,
        min_price=min_price,
        max_price=max_price,
        seller_id=seller_id,
    )

    return {
        "listings": [
            {
                "id": l.id,
                "movie_id": l.movie_id,
                "seller_id": l.seller_id,
                "title": l.title,
                "description": l.description,
                "tags": l.tags,
                "pricing_type": l.pricing_type.value,
                "base_price": l.base_price,
                "currency": l.currency,
                "status": l.status.value,
                "view_count": l.view_count,
                "purchase_count": l.purchase_count,
                "created_at": l.created_at.isoformat(),
            }
            for l in listings
        ]
    }


@router.post("")
async def create_listing(
    data: ListingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Create a new marketplace listing."""
    service = MarketplaceService(db)

    try:
        pricing_enum = PricingType(data.pricing_type)
    except ValueError:
        pricing_enum = PricingType.PURCHASE

    listing = await service.create_listing(
        movie_id=data.movie_id,
        seller_id=current_user.id,
        tenant_id=tenant_id,
        title=data.title,
        description=data.description,
        tags=data.tags,
        pricing_type=pricing_enum,
        base_price=data.base_price,
        currency=data.currency,
    )

    return {
        "id": listing.id,
        "movie_id": listing.movie_id,
        "title": listing.title,
        "status": listing.status.value,
    }


@router.get("/{listing_id}")
async def get_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get listing details."""
    service = MarketplaceService(db)
    listing = await service.get_listing_by_id(listing_id, tenant_id)

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    stats = await service.get_listing_stats(listing_id, tenant_id)

    return {
        "id": listing.id,
        "movie_id": listing.movie_id,
        "seller_id": listing.seller_id,
        "title": listing.title,
        "description": listing.description,
        "tags": listing.tags,
        "pricing_type": listing.pricing_type.value,
        "base_price": listing.base_price,
        "currency": listing.currency,
        "status": listing.status.value,
        "view_count": listing.view_count,
        "purchase_count": listing.purchase_count,
        "created_at": listing.created_at.isoformat(),
        "pricing_tiers": [
            {
                "id": t.id,
                "name": t.name,
                "price": t.price,
                "duration_days": t.duration_days,
                "features": t.features,
            }
            for t in listing.pricing_tiers
        ],
        "previews": [
            {
                "id": p.id,
                "preview_type": p.preview_type.value,
                "video_url": p.video_url,
                "thumbnail_url": p.thumbnail_url,
                "duration_seconds": p.duration_seconds,
            }
            for p in listing.previews
        ],
        "stats": stats,
    }


@router.put("/{listing_id}")
async def update_listing(
    listing_id: int,
    data: ListingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Update a listing (owner only)."""
    service = MarketplaceService(db)

    update_data = data.model_dump(exclude_unset=True)
    listing = await service.update_listing(
        listing_id=listing_id,
        tenant_id=tenant_id,
        seller_id=current_user.id,
        **update_data,
    )

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found or not authorized")

    return {"message": "Listing updated", "id": listing.id}


@router.delete("/{listing_id}")
async def delete_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Delete a listing (owner only)."""
    service = MarketplaceService(db)

    success = await service.delete_listing(
        listing_id=listing_id,
        tenant_id=tenant_id,
        seller_id=current_user.id,
    )

    if not success:
        raise HTTPException(status_code=404, detail="Listing not found or not authorized")

    return {"message": "Listing deleted"}


@router.post("/{listing_id}/purchase")
async def purchase_license(
    listing_id: int,
    data: PurchaseRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Purchase a license for a listing."""
    service = MarketplaceService(db)

    try:
        license_obj = await service.purchase_license(
            listing_id=listing_id,
            buyer_id=current_user.id,
            tenant_id=tenant_id,
            tier_id=data.tier_id,
            transaction_id=data.transaction_id,
        )
        return {
            "license_id": license_obj.id,
            "license_type": license_obj.license_type,
            "price_paid": license_obj.price_paid,
            "valid_until": license_obj.valid_until.isoformat() if license_obj.valid_until else None,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/licenses/me")
async def get_my_licenses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get current user's licenses."""
    service = MarketplaceService(db)
    licenses = await service.get_user_licenses(current_user.id, tenant_id)

    return {
        "licenses": [
            {
                "id": l.id,
                "listing_id": l.listing_id,
                "license_type": l.license_type,
                "price_paid": l.price_paid,
                "currency": l.currency,
                "valid_from": l.valid_from.isoformat(),
                "valid_until": l.valid_until.isoformat() if l.valid_until else None,
                "status": l.status.value,
            }
            for l in licenses
        ]
    }


@router.post("/{listing_id}/tiers")
async def add_pricing_tier(
    listing_id: int,
    data: PricingTierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Add a pricing tier to a listing (owner only)."""
    service = MarketplaceService(db)

    # Verify ownership
    listing = await service.get_listing_by_id(listing_id, tenant_id)
    if not listing or listing.seller_id != current_user.id:
        raise HTTPException(status_code=404, detail="Listing not found or not authorized")

    tier = await service.add_pricing_tier(
        listing_id=listing_id,
        name=data.name,
        price=data.price,
        duration_days=data.duration_days,
        features=data.features,
    )

    return {"id": tier.id, "name": tier.name, "price": tier.price}


@router.post("/{listing_id}/previews")
async def add_preview(
    listing_id: int,
    data: PreviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Add a preview to a listing (owner only)."""
    service = MarketplaceService(db)

    # Verify ownership
    listing = await service.get_listing_by_id(listing_id, tenant_id)
    if not listing or listing.seller_id != current_user.id:
        raise HTTPException(status_code=404, detail="Listing not found or not authorized")

    try:
        preview_enum = PreviewType(data.preview_type)
    except ValueError:
        preview_enum = PreviewType.TRAILER

    preview = await service.add_preview(
        listing_id=listing_id,
        preview_type=preview_enum,
        video_url=data.video_url,
        thumbnail_url=data.thumbnail_url,
        duration_seconds=data.duration_seconds,
    )

    return {"id": preview.id, "preview_type": preview.preview_type.value}


@router.post("/{listing_id}/reviews")
async def add_review(
    listing_id: int,
    data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(get_tenant_id),
):
    """Add a review to a listing."""
    service = MarketplaceService(db)

    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    review = await service.add_review(
        listing_id=listing_id,
        user_id=current_user.id,
        tenant_id=tenant_id,
        rating=data.rating,
        title=data.title,
        content=data.content,
    )

    return {"id": review.id, "rating": review.rating}


@router.get("/{listing_id}/reviews")
async def get_reviews(
    listing_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
):
    """Get reviews for a listing."""
    service = MarketplaceService(db)
    reviews = await service.get_reviews(listing_id, tenant_id, skip, limit)

    return {
        "reviews": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "rating": r.rating,
                "title": r.title,
                "content": r.content,
                "helpful_count": r.helpful_count,
                "created_at": r.created_at.isoformat(),
            }
            for r in reviews
        ]
    }
