# Phase 15 Context: Ratings and Reviews

## Phase Overview
Goal: Add movie ratings and reviews features for user engagement

Requirements:
- SOC-01: Movie Ratings
- SOC-02: Movie Reviews

Depends on: Phase 3 (User Catalog and Playback), Phase 4 (Frontend Integration)

## Technical Approach

### SOC-01: Movie Ratings
- Rating model: user_id, movie_id, rating (1-5), created_at, updated_at
- Unique constraint: one rating per user per movie
- Calculate average rating and count on movie queries
- Show user rating on movie cards when logged in

### SOC-02: Movie Reviews
- Review model: user_id, movie_id, content, created_at, updated_at
- One review per user per movie
- Display reviews on movie detail page with pagination
- Allow edit/delete by review author
