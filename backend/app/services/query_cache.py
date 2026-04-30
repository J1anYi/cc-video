"""Query result caching layer."""
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Any, Callable
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class QueryCache:
    """In-memory query result cache with TTL support."""

    def __init__(self, default_ttl: int = 300):
        self._cache: dict[str, tuple[Any, datetime]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a cache key from function arguments."""
        key_data = json.dumps({"args": str(args), "kwargs": str(kwargs)}, sort_keys=True)
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"{prefix}:{key_hash}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key in self._cache:
            value, expiry = self._cache[key]
            if datetime.utcnow() < expiry:
                self.hits += 1
                return value
            else:
                del self._cache[key]
        self.misses += 1
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL."""
        expiry = datetime.utcnow() + timedelta(seconds=ttl or self.default_ttl)
        self._cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]

    def clear_prefix(self, prefix: str) -> int:
        """Clear all keys with given prefix."""
        keys_to_delete = [k for k in self._cache if k.startswith(prefix)]
        for key in keys_to_delete:
            del self._cache[key]
        return len(keys_to_delete)

    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "size": len(self._cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 2),
        }


# Global query cache instance
query_cache = QueryCache()


def cached_query(prefix: str, ttl: int = 300):
    """Decorator for caching query results."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = query_cache._generate_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_result = query_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {prefix}")
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                query_cache.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator


def invalidate_cache(prefix: str) -> int:
    """Invalidate all cache entries with given prefix."""
    return query_cache.clear_prefix(prefix)
