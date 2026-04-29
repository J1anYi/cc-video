# Roadmap: CC Video v1.1

**Created:** 2026-04-29
**Granularity:** Coarse
**Core Value:** Users can reliably browse the movie list and play administrator-uploaded videos through the web app.

## Overview

| Phase | Name | Goal | Requirements | UI hint |
|-------|------|------|--------------|---------|
| 5 | Movie Search & Filtering | Add search and category filtering to the movie catalog | DISC-01, DISC-02, DISC-03 | yes |
| 6 | User Registration | Enable self-registration for new users | ACC-01, ACC-02, ACC-03 | yes |

## Phase Details

### Phase 5: Movie Search & Filtering

**Goal:** Enable users to find movies quickly through title search and category/genre filtering.

**Requirements:** DISC-01, DISC-02, DISC-03

**Success Criteria:**

1. User can type in a search box to filter movies by title (case-insensitive, partial match)
2. User can select a category/genre to filter the catalog
3. Search and filter can be combined for refined results
4. Empty search state shows helpful message when no results match
5. Catalog updates dynamically as user types or selects filters

**Notes:**

- Backend needs to support query parameters for search (q) and category filter
- Movie model may need a category/genre field added (check existing schema)
- Frontend needs search input and filter UI in catalog header
- Consider debouncing search input for performance

### Phase 6: User Registration

**Goal:** Allow new users to create accounts without admin intervention.

**Requirements:** ACC-01, ACC-02, ACC-03

**Success Criteria:**

1. Public registration page is accessible without login
2. Registration form collects username and password with validation
3. Username uniqueness is validated before account creation
4. Password meets minimum strength requirements
5. Successful registration redirects to login or auto-logs in
6. New users have the default "user" role (not admin)

**Notes:**

- Backend needs a public registration endpoint
- Consider rate limiting to prevent abuse
- Login page should link to registration
- Registration page should link back to login

## Coverage Validation

| Requirement | Phase | Status |
|-------------|-------|--------|
| DISC-01 | Phase 5 | ⏳ Pending |
| DISC-02 | Phase 5 | ⏳ Pending |
| DISC-03 | Phase 5 | ⏳ Pending |
| ACC-01 | Phase 6 | ⏳ Pending |
| ACC-02 | Phase 6 | ⏳ Pending |
| ACC-03 | Phase 6 | ⏳ Pending |

**Coverage:**
- v1.1 requirements: 6 total
- Mapped to phases: 6
- Unmapped: 0
- Completed: 0
- Remaining: 6

---
*Roadmap created: 2026-04-29 for v1.1 milestone*
