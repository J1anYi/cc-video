# PLAN: Phase 23 - Advanced Search

**Milestone:** v1.9 Admin & Safety
**Phase:** 23
**Goal:** Implement advanced search filters for movies

## Requirements

- SEARCH-01: User can filter movies by minimum rating
- SEARCH-02: User can filter movies by release year range
- SEARCH-03: User can filter movies by duration range
- SEARCH-04: User can combine multiple filters
- SEARCH-05: User can sort search results (rating, year, title)

## Success Criteria

1. User can filter by rating threshold
2. User can filter by year range
3. User can combine multiple filters
4. Sort options work correctly
5. Filters persist across pagination

## Implementation Plan

### Task 1: Backend - Movie Model Fields
- Add release_year field to Movie model (nullable)
- Add duration_minutes field to Movie model (nullable)
- Create migration for new fields

### Task 2: Backend - Enhanced Search API
- Update GET /api/movies to accept filter params
- min_rating, year_from, year_to, duration_from, duration_to
- sort_by param (rating, year, title, created_at)
- sort_order param (asc, desc)

### Task 3: Backend - Admin Movie Edit
- Update admin movie edit to include year and duration
- Allow bulk update for existing movies

### Task 4: Frontend - Filter UI
- Add filter panel to catalog page
- Rating slider or dropdown
- Year range inputs
- Duration range inputs
- Sort dropdown

### Task 5: Frontend - URL Params
- Store filters in URL query params
- Shareable filter URLs
- Reset filters button

### Task 6: Frontend - Mobile Filters
- Collapsible filter panel on mobile
- Apply filters button
- Active filter badges

## Dependencies

- Existing Movie model
- Existing search functionality
- Existing catalog page

## Risks

- Performance: Index new fields for filtering
- Data migration: Existing movies will have null values

---
*Phase plan created: 2026-04-30*
