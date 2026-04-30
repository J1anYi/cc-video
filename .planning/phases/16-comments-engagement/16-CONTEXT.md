# Phase 16 Context: Comments and Engagement

## Phase Overview
Goal: Add comments on reviews and helpful votes for user engagement

Requirements:
- SOC-03: Comments on Reviews
- SOC-04: Helpful Votes

Depends on: Phase 15 (Ratings and Reviews)

## Technical Approach

### SOC-03: Comments on Reviews
- Comment model: user_id, review_id, content, created_at
- Multiple comments per review
- Display comments thread below review
- Allow delete by comment author

### SOC-04: Helpful Votes
- HelpfulVote model: user_id, review_id, created_at
- One vote per user per review
- Display helpful count on review
- Toggle vote on/off
