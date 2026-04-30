# Plan: Phase 131 - GraphQL API

## Overview
Implement GraphQL API layer using Strawberry GraphQL alongside existing REST API.

## Tasks

### 1. Install Dependencies (GQL-01)
- Add strawberry-graphql[fastapi] to requirements
- Add strawberry-graphql[debug-toolbar] for development

### 2. Define Schema (GQL-01)
- Create `backend/app/graphql/schema.py`
- Define types for User, Movie, Rating, Review
- Define input types for mutations

### 3. Query Resolvers (GQL-02)
- Create `backend/app/graphql/queries/`
- User queries (me, user, users)
- Movie queries (movie, movies, search)
- Rating queries (ratings, user_ratings)
- Review queries (reviews, movie_reviews)

### 4. Mutation Resolvers (GQL-02)
- Create `backend/app/graphql/mutations/`
- Auth mutations (login, register)
- User mutations (update_profile)
- Rating mutations (create_rating, update_rating)
- Review mutations (create_review, update_review)

### 5. Subscriptions (GQL-03)
- Create `backend/app/graphql/subscriptions/`
- Notification subscription
- Real-time rating updates
- Watch party updates

### 6. Federation (GQL-04)
- Configure federation entities
- Define entity resolvers
- Set up federation schema

### 7. Playground (GQL-05)
- Mount GraphQL endpoint in main.py
- Enable GraphQL playground in development
- Add authentication middleware

## Files to Create

- `backend/app/graphql/__init__.py`
- `backend/app/graphql/schema.py`
- `backend/app/graphql/types/` (user.py, movie.py, rating.py, review.py)
- `backend/app/graphql/queries/` (user.py, movie.py, rating.py, review.py)
- `backend/app/graphql/mutations/` (auth.py, user.py, rating.py, review.py)
- `backend/app/graphql/subscriptions/` (notifications.py, ratings.py)

## Success Criteria
1. GraphQL endpoint accessible at /graphql
2. Queries return correct data
3. Mutations modify data correctly
4. Subscriptions stream real-time updates
5. Playground available in development

---
*Created: 2026-05-01*
