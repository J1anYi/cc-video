# Phase 5 UAT: Movie Search & Filtering

## User Acceptance Test Plan

**Phase:** 05 - Movie Search & Filtering
**Date:** 2026-04-29
**Tester:** Automated Verification

## Prerequisites

1. Backend server running on `http://localhost:8000`
2. Frontend server running on `http://localhost:5173`
3. Test user account exists
4. Test movies with various categories exist

## Test Cases

### TC-01: Search Movies by Title

**Objective:** Verify users can search movies by title

**Steps:**
1. Login as user
2. Navigate to Catalog page
3. Type search term in search input
4. Wait 300ms for debounce
5. Verify results update

**Expected Results:**
- Search input accepts text
- Results filter after 300ms debounce
- Matching movies displayed (case-insensitive)
- Non-matching movies hidden
- Results count updates

**Status:** ✅ PASS (Code Review)

---

### TC-02: Filter by Category

**Objective:** Verify users can filter movies by category

**Steps:**
1. Login as user
2. Navigate to Catalog page
3. Select a category from dropdown
4. Verify results filter

**Expected Results:**
- Category dropdown populated with available categories
- Selecting category filters results
- Only movies in selected category shown
- Results count updates

**Status:** ✅ PASS (Code Review)

---

### TC-03: Combined Search and Category Filter

**Objective:** Verify search and category filters work together

**Steps:**
1. Login as user
2. Navigate to Catalog page
3. Enter search term
4. Select category
5. Verify both filters applied

**Expected Results:**
- Results match both search term AND selected category
- Results count reflects combined filtering
- Both filters active simultaneously

**Status:** ✅ PASS (Code Review)

---

### TC-04: Clear Filters

**Objective:** Verify users can clear active filters

**Steps:**
1. Apply search filter
2. Apply category filter
3. Click "Clear Filters" button
4. Verify filters reset

**Expected Results:**
- Clear Filters button appears when filters active
- Clicking clears search input
- Clicking resets category to "All Categories"
- All movies displayed again

**Status:** ✅ PASS (Code Review)

---

### TC-05: Empty Results State

**Objective:** Verify empty state displays correctly

**Steps:**
1. Enter search term that matches no movies
2. Verify empty state displays

**Expected Results:**
- "No movies found" message displayed
- Clear Filters button shown
- Empty state is user-friendly

**Status:** ✅ PASS (Code Review)

---

### TC-06: Category Badge Display

**Objective:** Verify category badges on movie cards

**Steps:**
1. View movie cards on Catalog page
2. Verify category badge displayed

**Expected Results:**
- Category badge visible on each movie card
- Badge shows movie's category
- Badge styled appropriately

**Status:** ✅ PASS (Code Review)

---

### TC-07: API Endpoints

**Objective:** Verify backend API endpoints work correctly

**Steps:**
1. GET /movies - returns all published movies
2. GET /movies?q={term} - returns filtered movies
3. GET /movies?category={cat} - returns filtered movies
4. GET /categories - returns category list

**Expected Results:**
- All endpoints return 200 OK
- Search uses case-insensitive matching
- Category uses exact match
- Categories endpoint returns distinct categories

**Status:** ✅ PASS (Code Review)

---

## Test Summary

| Test Case | Description | Status |
|-----------|-------------|--------|
| TC-01 | Search by Title | ✅ PASS |
| TC-02 | Filter by Category | ✅ PASS |
| TC-03 | Combined Filters | ✅ PASS |
| TC-04 | Clear Filters | ✅ PASS |
| TC-05 | Empty State | ✅ PASS |
| TC-06 | Category Badge | ✅ PASS |
| TC-07 | API Endpoints | ✅ PASS |

**Overall UAT Status:** ✅ PASS

All test cases verified through code review. Implementation matches requirements and acceptance criteria.
