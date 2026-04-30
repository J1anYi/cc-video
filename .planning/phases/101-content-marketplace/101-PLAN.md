# Phase 101: Content Marketplace - Plan

**Phase:** 101
**Milestone:** v3.4 Content Ecosystem & Marketplace
**Date:** 2026-04-30

## Goal

Implement a content marketplace where users can browse, license, and purchase content with various pricing models.

## Tasks

### 1. Backend Models (backend/app/models/marketplace.py)

- [ ] Create MarketplaceListing model
  - id, movie_id, seller_id, tenant_id
  - title, description, tags
  - pricing_type (per_view, subscription, purchase)
  - base_price, currency
  - status (active, inactive, sold_out)
  - created_at, updated_at

- [ ] Create License model
  - id, listing_id, buyer_id, tenant_id
  - license_type, price_paid
  - valid_from, valid_until
  - status (active, expired, revoked)
  - created_at

- [ ] Create PricingTier model
  - id, listing_id
  - name, price, duration_days
  - features (JSON)
  - created_at

- [ ] Create ContentPreview model
  - id, listing_id
  - preview_type (trailer, clip, sample)
  - video_url, duration_seconds
  - created_at

- [ ] Create MarketplaceReview model
  - id, listing_id, user_id, tenant_id
  - rating, title, content
  - helpful_count
  - created_at, updated_at

### 2. Backend Service (backend/app/services/marketplace_service.py)

- [ ] Create MarketplaceService class
  - create_listing()
  - get_listings() with search/filter
  - get_listing_by_id()
  - update_listing()
  - delete_listing()
  - purchase_license()
  - get_user_licenses()
  - add_review()
  - get_reviews()

### 3. Backend Routes (backend/app/routes/marketplace.py)

- [ ] GET /marketplace - Browse listings
- [ ] POST /marketplace - Create listing (auth required)
- [ ] GET /marketplace/{id} - Get listing details
- [ ] PUT /marketplace/{id} - Update listing (owner only)
- [ ] DELETE /marketplace/{id} - Delete listing (owner only)
- [ ] POST /marketplace/{id}/purchase - Purchase license
- [ ] GET /marketplace/licenses - Get user's licenses
- [ ] POST /marketplace/{id}/reviews - Add review
- [ ] GET /marketplace/{id}/reviews - Get reviews

### 4. Frontend API Client (frontend/src/api/marketplace.ts)

- [ ] getListings(params)
- [ ] createListing(data)
- [ ] getListing(id)
- [ ] updateListing(id, data)
- [ ] deleteListing(id)
- [ ] purchaseLicense(id, data)
- [ ] getUserLicenses()
- [ ] addReview(id, data)
- [ ] getReviews(id)

### 5. Frontend Components

- [ ] ContentMarketplace.tsx - Main marketplace page
- [ ] ListingCard.tsx - Listing preview card
- [ ] ListingDetail.tsx - Full listing view
- [ ] CreateListing.tsx - Create listing form
- [ ] PurchaseModal.tsx - Purchase dialog

## Success Criteria

1. Users can browse marketplace listings
2. Content owners can create listings with pricing
3. Users can purchase licenses
4. Users can leave reviews
5. Search and filtering works

## Files to Create/Modify

- backend/app/models/marketplace.py (new)
- backend/app/services/marketplace_service.py (new)
- backend/app/routes/marketplace.py (new)
- backend/app/main.py (add router)
- frontend/src/api/marketplace.ts (new)
- frontend/src/routes/marketplace/ContentMarketplace.tsx (new)

---
*Created: 2026-04-30*
