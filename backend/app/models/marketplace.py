"""Marketplace models for content marketplace."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Table, Column
import enum

from app.database import Base


class PricingType(enum.Enum):
    PER_VIEW = "per_view"
    SUBSCRIPTION = "subscription"
    PURCHASE = "purchase"


class ListingStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SOLD_OUT = "sold_out"


class LicenseStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


class PreviewType(enum.Enum):
    TRAILER = "trailer"
    CLIP = "clip"
    SAMPLE = "sample"


class MarketplaceListing(Base):
    """Marketplace listing for content."""
    __tablename__ = "marketplace_listings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    pricing_type: Mapped[PricingType] = mapped_column(
        SQLEnum(PricingType), 
        default=PricingType.PURCHASE
    )
    base_price: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    status: Mapped[ListingStatus] = mapped_column(
        SQLEnum(ListingStatus), 
        default=ListingStatus.ACTIVE
    )
    
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    purchase_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pricing_tiers: Mapped[List["PricingTier"]] = relationship(
        "PricingTier", 
        back_populates="listing",
        cascade="all, delete-orphan"
    )
    previews: Mapped[List["ContentPreview"]] = relationship(
        "ContentPreview", 
        back_populates="listing",
        cascade="all, delete-orphan"
    )
    reviews: Mapped[List["MarketplaceReview"]] = relationship(
        "MarketplaceReview", 
        back_populates="listing",
        cascade="all, delete-orphan"
    )
    licenses: Mapped[List["License"]] = relationship(
        "License", 
        back_populates="listing",
        cascade="all, delete-orphan"
    )


class PricingTier(Base):
    """Pricing tier for a listing."""
    __tablename__ = "pricing_tiers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("marketplace_listings.id"), nullable=False)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    features: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    listing: Mapped["MarketplaceListing"] = relationship("MarketplaceListing", back_populates="pricing_tiers")


class License(Base):
    """License for purchased content."""
    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("marketplace_listings.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    license_type: Mapped[str] = mapped_column(String(50), nullable=False)
    price_paid: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    valid_from: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    valid_until: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    status: Mapped[LicenseStatus] = mapped_column(
        SQLEnum(LicenseStatus), 
        default=LicenseStatus.ACTIVE
    )
    
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    listing: Mapped["MarketplaceListing"] = relationship("MarketplaceListing", back_populates="licenses")


class ContentPreview(Base):
    """Content preview (trailer, clip, sample)."""
    __tablename__ = "content_previews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("marketplace_listings.id"), nullable=False)
    
    preview_type: Mapped[PreviewType] = mapped_column(
        SQLEnum(PreviewType), 
        default=PreviewType.TRAILER
    )
    video_url: Mapped[str] = mapped_column(String(500), nullable=False)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    listing: Mapped["MarketplaceListing"] = relationship("MarketplaceListing", back_populates="previews")


class MarketplaceReview(Base):
    """Review for marketplace listing."""
    __tablename__ = "marketplace_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("marketplace_listings.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tenant_id: Mapped[int] = mapped_column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    helpful_count: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    listing: Mapped["MarketplaceListing"] = relationship("MarketplaceListing", back_populates="reviews")
