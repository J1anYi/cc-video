# Phase 5: Movie Search & Filtering - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-29
**Phase:** 05-movie-search-filtering
**Areas discussed:** Search trigger, Search scope, Category field, Backend query, UI placement, Empty state

---

## Search Trigger Method

| Option | Description | Selected |
|--------|-------------|----------|
| Debounced real-time search | 300ms delay after typing stops, auto-requests | ✓ |
| Submit-based search | User presses Enter or clicks button | |

**User's choice:** Debounced real-time search (auto-selected)
**Notes:** Better UX, standard pattern for search inputs

---

## Search Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Title only | Case-insensitive partial match on title | ✓ |
| Title + description | Search both fields | |

**User's choice:** Title only (auto-selected)
**Notes:** Simpler query, faster results, matches DISC-01 requirement

---

## Category Field Design

| Option | Description | Selected |
|--------|-------------|----------|
| String field (optional) | Simple text field, flexible categories | ✓ |
| Enum field | Predefined categories | |
| Separate Category table | Normalized, many-to-many | |

**User's choice:** String field (optional) (auto-selected)
**Notes:** Flexibility without complexity, existing movies work without category

---

## Backend Query Design

| Option | Description | Selected |
|--------|-------------|----------|
| Query parameters on GET /movies | ?q= and ?category= params | ✓ |
| Separate search endpoint | POST /movies/search | |

**User's choice:** Query parameters on GET /movies (auto-selected)
**Notes:** RESTful, matches existing endpoint pattern, both params combinable

---

## UI Placement

| Option | Description | Selected |
|--------|-------------|----------|
| Catalog page header | Above movie grid | ✓ |
| Sidebar filter panel | Separate filter column | |
| Modal search dialog | Overlay search UI | |

**User's choice:** Catalog page header (auto-selected)
**Notes:** Natural location, matches existing layout structure

---

## Empty State

| Option | Description | Selected |
|--------|-------------|----------|
| Friendly message + Clear button | "No results found" + clear filters action | ✓ |
| Simple text only | "No movies found" | |

**User's choice:** Friendly message + Clear button (auto-selected)
**Notes:** Helps user understand and recover

---

## Claude's Discretion

- Exact debounce timing (300-500ms acceptable)
- Category dropdown styling
- Search input placeholder text
- Loading state during search

## Deferred Ideas

None — discussion stayed within phase scope.
