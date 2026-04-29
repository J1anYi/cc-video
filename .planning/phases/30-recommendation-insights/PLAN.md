# PLAN: Phase 30 - Recommendation Insights

**Milestone:** v1.10 Analytics & Insights
**Phase:** 30
**Goal:** Provide transparency and control over recommendation system

## Requirements

- REC-01: User can see why movies are recommended
- REC-02: User can view recommendation preferences
- REC-03: User can adjust recommendation factors
- REC-04: User can see similarity scores for recommendations
- REC-05: User can provide feedback on recommendations

## Success Criteria

1. Recommendations show explanation badges
2. Preference page shows current factors
3. Users can adjust factor weights
4. Similarity scores visible on recommended items
5. Feedback mechanism improves future recommendations

## Implementation Plan

### Task 1: Backend - Recommendation Explanation
- Extend recommendation algorithm to track reasons
- Reason types: genre_match, watch_history, similar_users, trending
- Include reason in API response

### Task 2: Backend - Recommendation Preferences Model
- Create `UserRecommendationPrefs` model
- Fields: genre_weights, recency_weight, social_weight
- Default values for new users

### Task 3: Backend - Recommendation API Extensions
- GET /api/recommendations?include_reasons=true
- GET /api/users/me/recommendation-preferences
- PATCH /api/users/me/recommendation-preferences
- POST /api/recommendations/{movieId}/feedback

### Task 4: Backend - Feedback Processing
- Accept feedback types: interested, not_interested, seen
- Store feedback for algorithm improvement
- Adjust future recommendations

### Task 5: Backend - Similarity Score
- Calculate movie similarity scores
- Score factors: genre, director, actors, user behavior
- Include in recommendation responses

### Task 6: Frontend - Recommendation Explanation UI
- Show "Why recommended?" badge on movie cards
- Tooltip or modal with explanation
- Similarity percentage display

### Task 7: Frontend - Preferences Page
- Create `/settings/recommendations` route
- Sliders for factor weights
- Genre preference toggles
- Save/reset buttons

### Task 8: Frontend - Feedback Buttons
- "Interested" / "Not interested" buttons
- Inline feedback on recommendations
- Quick actions without navigation

### Task 9: Frontend - Similarity Display
- Show similarity score as percentage
- Visual indicator (progress bar)
- Comparison points (genres in common, etc.)

### Task 10: Integration Testing
- Test recommendation explanations
- Test preference updates
- Test feedback processing
- Verify improved recommendations

## Dependencies

- Recommendation system (Phase 13)
- User watch history
- Genre metadata

## Risks

- Algorithm complexity: Making explanations simple but accurate
- Mitigation: High-level reasons, not technical details
- Cold start: New users have no preferences
- Mitigation: Smart defaults, onboarding

---
*Phase plan created: 2026-04-30*
