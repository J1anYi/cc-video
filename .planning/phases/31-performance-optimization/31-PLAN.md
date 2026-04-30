---
wave: 1
depends_on: []
files_modified:
  - backend/app/main.py
  - backend/app/routes/*.py
  - backend/app/models/*.py
  - frontend/src/App.tsx
  - frontend/src/main.tsx
requirements_addressed:
  - PERF-01
  - PERF-02
  - PERF-03
  - PERF-04
  - PERF-05
autonomous: true
---

# PLAN: Phase 31 - Performance Optimization

**Objective:** Optimize API responses, frontend load time, video streaming, database queries, and implement caching.

## Task 1: Database Query Optimization

<read_first>
- backend/app/models/movie.py
- backend/app/models/user.py
- backend/app/routes/movies.py
- backend/app/routes/auth.py
</read_first>

<action>
1. Add database indexes for frequently queried columns:
   - movies table: genre, created_at, avg_rating
   - users table: email, username, created_at
   - watch_history table: user_id, movie_id, watched_at
   - favorites table: user_id, movie_id
   - reviews table: movie_id, user_id, created_at

2. Use SQLAlchemy `Index` in model definitions:
```python
__table_args__ = (
    Index('ix_movies_genre', 'genre'),
    Index('ix_movies_created_at', 'created_at'),
    Index('ix_watch_history_user_watched', 'user_id', 'watched_at'),
)
```

3. Add EXPLAIN ANALYZE logging for slow queries in development.
</action>

<acceptance_criteria>
- backend/app/models/movie.py contains `Index(` definitions
- backend/app/models/user.py contains `Index(` definitions
- Database migration creates indexes
- Query performance improved (verify with EXPLAIN)
</acceptance_criteria>

---

## Task 2: API Response Caching Layer

<read_first>
- backend/app/main.py
- backend/app/routes/movies.py
- backend/app/routes/auth.py
</read_first>

<action>
1. Create caching service at `backend/app/services/cache.py`:
   - Use Redis or in-memory cache (dict with TTL)
   - Implement `get_cached(key)`, `set_cached(key, value, ttl)`
   - Cache key pattern: `movies:list:{page}:{genre}`

2. Add caching to frequently accessed endpoints:
   - GET /api/movies - cache movie list for 5 minutes
   - GET /api/movies/{id} - cache movie detail for 10 minutes
   - GET /api/recommendations - cache for 2 minutes

3. Invalidate cache on movie create/update/delete.
</action>

<acceptance_criteria>
- backend/app/services/cache.py exists with `get_cached`, `set_cached` functions
- backend/app/routes/movies.py uses caching
- Cache invalidation works on movie updates
- API response times under 200ms for cached endpoints
</acceptance_criteria>

---

## Task 3: Frontend Bundle Optimization

<read_first>
- frontend/vite.config.ts
- frontend/src/App.tsx
- frontend/src/main.tsx
</read_first>

<action>
1. Implement code splitting with lazy loading:
```tsx
const Catalog = lazy(() => import('./routes/Catalog'));
const Admin = lazy(() => import('./routes/admin/Dashboard'));
// etc for all routes
```

2. Add loading suspense component:
```tsx
<Suspense fallback={<LoadingSpinner />}>
  <Routes>...</Routes>
</Suspense>
```

3. Configure Vite for production optimization:
   - Enable gzip compression
   - Set build.chunkSizeWarningLimit
   - Enable manual chunks for vendor splitting
</action>

<acceptance_criteria>
- frontend/src/App.tsx uses `lazy()` for route imports
- frontend/vite.config.ts has build optimization config
- Initial bundle size reduced (check with `vite-bundle-visualizer`)
- Page load under 3 seconds
</acceptance_criteria>

---

## Task 4: Video Streaming Optimization

<read_first>
- backend/app/services/video_streaming.py
- backend/app/routes/movies.py
</read_first>

<action>
1. Implement HTTP range requests for video streaming:
   - Support `Range` header in video endpoint
   - Return `206 Partial Content` with proper headers
   - Set `Accept-Ranges: bytes` header

2. Add video buffering optimization:
   - Preload first 1MB of video
   - Use appropriate chunk sizes (1-2MB)

3. Add video file compression endpoint for admin uploads.
</action>

<acceptance_criteria>
- backend/app/routes/movies.py handles Range header
- Response includes `Accept-Ranges: bytes` header
- Video starts within 2 seconds
- Partial content (206) responses work correctly
</acceptance_criteria>

---

## Task 5: API Response Time Monitoring

<read_first>
- backend/app/main.py
- backend/app/routes/*.py
</read_first>

<action>
1. Add request timing middleware:
```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

2. Add logging for slow requests (>200ms).
3. Create health check endpoint with response time metrics.
</action>

<acceptance_criteria>
- backend/app/main.py has timing middleware
- Response headers include `X-Process-Time`
- Slow request logging works
- GET /api/health returns response time
</acceptance_criteria>

---

## Verification Criteria

1. **API Performance:**
   - [ ] All API endpoints respond under 200ms (95th percentile)
   - [ ] Cached endpoints respond under 50ms

2. **Frontend Performance:**
   - [ ] Initial page load under 3 seconds
   - [ ] Route transitions under 500ms

3. **Video Streaming:**
   - [ ] Video starts within 2 seconds
   - [ ] Range requests work correctly

4. **Database:**
   - [ ] Indexes created for key columns
   - [ ] Query plans show index usage

5. **Caching:**
   - [ ] Cache service implemented
   - [ ] Cache invalidation works

---

## must_haves

- Database indexes on all frequently queried columns
- Caching layer for movie list and detail endpoints
- Lazy loading for all frontend routes
- HTTP range support for video streaming
- Response time monitoring middleware
