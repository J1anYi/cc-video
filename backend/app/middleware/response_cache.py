"""Response caching middleware."""
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class ResponseCache:
    """In-memory response cache."""

    def __init__(self, default_ttl: int = 60):
        self._cache: dict[str, tuple[bytes, dict, datetime]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _generate_key(self, request: Request) -> str:
        key_data = {
            "method": request.method,
            "url": str(request.url),
        }
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()

    def get(self, key: str) -> Optional[tuple[bytes, dict]]:
        if key in self._cache:
            body, headers, expiry = self._cache[key]
            if datetime.utcnow() < expiry:
                self.hits += 1
                return body, headers
            else:
                del self._cache[key]
        self.misses += 1
        return None

    def set(self, key: str, body: bytes, headers: dict, ttl: Optional[int] = None) -> None:
        expiry = datetime.utcnow() + timedelta(seconds=ttl or self.default_ttl)
        self._cache[key] = (body, headers, expiry)

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> dict:
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "size": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
        }


response_cache = ResponseCache()


class ResponseCacheMiddleware(BaseHTTPMiddleware):
    """Middleware for caching GET responses."""

    def __init__(self, app, ttl: int = 60, cache_methods: list = None):
        super().__init__(app)
        self.ttl = ttl
        self.cache_methods = cache_methods or ["GET"]

    async def dispatch(self, request: Request, call_next):
        if request.method not in self.cache_methods:
            return await call_next(request)

        if "authorization" in request.headers:
            return await call_next(request)

        cache_key = response_cache._generate_key(request)
        cached = response_cache.get(cache_key)

        if cached:
            body, headers = cached
            return Response(content=body, headers={**headers, "X-Cache": "HIT"})

        response = await call_next(request)

        if response.status_code == 200:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            headers = dict(response.headers)
            headers.pop("content-length", None)
            response_cache.set(cache_key, body, headers, self.ttl)

            return Response(content=body, headers={**headers, "X-Cache": "MISS"}, status_code=200)

        return response
