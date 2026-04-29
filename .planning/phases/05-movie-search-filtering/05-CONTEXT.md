# Phase 5: Movie Search & Filtering - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase adds search and category filtering capabilities to the movie catalog, enabling users to find movies quickly as the catalog grows.

**In scope:**
- Backend: Add category field to Movie model
- Backend: Search endpoint with query parameters (q, category)
- Frontend: Search input with debounced input
- Frontend: Category filter dropdown
- Frontend: Empty state for no results
- Frontend: Combined search + filter support

**Out of scope:**
- User registration (Phase 6)
- Advanced filtering (tags, year, rating)
- Search suggestions/autocomplete
- Search history

</domain>

<decisions>
## Implementation Decisions

### Search Trigger Method
- **D-01:** Use **debounced real-time search** (300ms delay)
  - Rationale: Better UX than submit button, debounce prevents excessive API calls. Standard pattern for search inputs.
  - [auto] Selected as recommended for search UX.

### Search Scope
- **D-02:** Search **title only** (case-insensitive, partial match)
  - Rationale: Simpler query, faster results, matches DISC-01 requirement. Description search can be added later if needed.
  - [auto] Selected for simplicity and performance.

### Category Field Design
- **D-03:** Add **category field** to Movie model (String, optional)
  - Rationale: Simple string field allows flexible categories without enum constraints. Optional field - existing movies work without category.
  - [auto] Selected for flexibility.

### Backend Query Design
- **D-04:** Extend **GET /movies** with query parameters `?q=` and `?category=`
  - Rationale: RESTful, matches existing endpoint pattern. Both parameters optional and combinable.
  - [auto] Selected as RESTful pattern.

### UI Placement
- **D-05:** Search and filter controls in **Catalog page header** (above movie grid)
  - Rationale: Natural location, matches existing layout structure. Single row: search input + category dropdown.
  - [auto] Selected for layout consistency.

### Empty State
- **D-06:** Show **friendly message + "Clear filters" button** when no results
  - Rationale: Helps user understand why no results and provides easy recovery.
  - [auto] Selected for better UX.

### Claude's Discretion
- Exact debounce timing (300-500ms acceptable)
- Category dropdown styling
- Search input placeholder text
- Loading state during search

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Documentation
- `.planning/PROJECT.md` — Project vision, constraints, key decisions
- `.planning/REQUIREMENTS.md` — DISC-01, DISC-02, DISC-03 requirements
- `.planning/ROADMAP.md` — Phase 5 goal and success criteria

### Prior Phase Context
- `.planning/phases/03-user-catalog-playback/03-CONTEXT.md` — Phase 3 decisions (user catalog API)
- `.planning/phases/04-frontend-integration/04-CONTEXT.md` — Phase 4 decisions (frontend patterns)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `frontend/src/routes/Catalog.tsx` — Existing catalog page to extend
- `frontend/src/api/movies.ts` — API client to extend with search params
- `backend/app/services/movie.py` — movie_service with get_published() to extend
- `backend/app/models/movie.py` — Movie model to add category field
- `backend/app/schemas/movie.py` — Schemas to update

### Established Patterns
- React useState for local state
- useEffect for data fetching
- fetch API for HTTP requests
- FastAPI query parameters via function args
- SQLAlchemy select() with where() clauses

### Integration Points
- GET /movies endpoint — add q and category query params
- Catalog.tsx — add search input and category filter
- Movie model — add category column (migration needed)

</code_context>

<specifics>
## Specific Ideas

- Search should feel instant (debounced, not submit button)
- Category filter should show all available categories
- Clear filters button when filters are active
- Show "X results" count when filtering

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 05-movie-search-filtering*
*Context gathered: 2026-04-29*
