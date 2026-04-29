# Scalability Configuration

This document describes the scalability features implemented in Phase 32.

## SCALE-01: Horizontal Scaling Support

### Stateless Architecture

The backend is designed to be stateless, enabling horizontal scaling:

1. **No in-memory sessions**: All session data is stored in JWT tokens
2. **Cache compatible**: The caching layer can be migrated from in-memory to Redis
3. **File storage**: Videos and uploads stored on shared filesystem or object storage

### Load Balancer Configuration

Configure your load balancer with these health checks:

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `/health` | General health check | 200 OK |
| `/healthz` | Liveness probe | 200 OK |
| `/readyz` | Readiness probe | 200 OK or 503 |

Example Nginx configuration:
```nginx
upstream backend {
    least_conn;
    server backend1:8000 max_fails=3 fail_timeout=30s;
    server backend2:8000 max_fails=3 fail_timeout=30s;
    server backend3:8000 max_fails=3 fail_timeout=30s;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## SCALE-02: Database Connection Pooling

Connection pooling is configured in `app/database.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `DATABASE_POOL_SIZE` | 10 | Connections maintained in pool |
| `DATABASE_MAX_OVERFLOW` | 20 | Extra connections during peak |
| `DATABASE_POOL_TIMEOUT` | 30s | Wait time for connection |
| `DATABASE_POOL_RECYCLE` | 3600s | Recycle connections after 1 hour |

Override via environment variables:
```bash
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600
```

## SCALE-03: Static Asset CDN Integration

### Current Setup
Static files (posters, subtitles) are served directly by FastAPI in development.

### Production CDN Setup

1. Configure CDN origin to point to `/uploads/` path
2. Set cache headers:
   - Posters: Cache-Control: public, max-age=86400 (1 day)
   - Subtitles: Cache-Control: public, max-age=3600 (1 hour)
   - Videos: Cache-Control: public, max-age=31536000 (1 year)

3. For video files, use signed URLs for access control

## SCALE-04: Rate Limiting

Rate limiting is enforced on all public endpoints.

### Default Limits

| Endpoint Type | Limit | Window |
|---------------|-------|--------|
| Login | 5 requests | 60 seconds |
| Register | 3 requests | 60 seconds |
| Forgot Password | 3 requests | 300 seconds |
| Public API | 100 requests | 60 seconds |
| Authenticated API | 300 requests | 60 seconds |
| Admin API | 500 requests | 60 seconds |

### Rate Limit Headers

All responses include:
- `X-RateLimit-Limit`: Maximum requests per window
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when window resets

### Multi-Instance Note

Current implementation uses in-memory storage. For multi-instance deployment,
migrate to Redis-backed rate limiting:

```python
# TODO: Replace with Redis
# self._rate_limits = redis_client
```

## SCALE-05: Graceful Degradation

### Circuit Breaker Pattern

The `CircuitBreaker` class in `app/services/circuit_breaker.py` provides:

1. **Failure detection**: Trips after 5 consecutive failures
2. **Fast fail**: Rejects requests for 30 seconds after tripping
3. **Recovery**: Tests recovery with limited requests
4. **Fallback support**: Optional fallback function when circuit is open

Usage example:
```python
from app.services.circuit_breaker import get_circuit_breaker

async def fetch_external_data():
    # External API call
    pass

async def fallback_data():
    return {"data": "cached", "source": "fallback"}

breaker = get_circuit_breaker("external-api")
result = await breaker.call(fetch_external_data, fallback=fallback_data)
```

### Degradation Strategies

| Feature | Degradation Strategy |
|---------|---------------------|
| Recommendations | Return cached/popular content |
| External APIs | Return cached data or empty results |
| Analytics | Queue for async processing |
| Notifications | Batch and defer |

---

## Monitoring & Alerts

Recommended metrics to monitor:

1. **Connection Pool Usage**: Alert at 80% capacity
2. **Rate Limit Hits**: Alert if rate limits triggered frequently
3. **Circuit Breaker State**: Alert when circuit opens
4. **Response Time**: Alert if p95 > 500ms
5. **Error Rate**: Alert if > 5% of requests fail

---

*Phase 32 documentation - 2026-04-30*
