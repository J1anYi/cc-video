"""
Caching service for API response optimization.
Uses in-memory cache with TTL support.
"""

import time
from typing import Any, Optional
from functools import wraps


# In-memory cache store
_cache: dict[str, tuple[Any, float]] = {}  # key -> (value, expiry_time)


def get_cached(key: str) -> Optional[Any]:
    """Get a value from cache if it exists and hasn't expired."""
    if key in _cache:
        value, expiry = _cache[key]
        if time.time() < expiry:
            return value
        else:
            # Expired, remove it
            del _cache[key]
    return None


def set_cached(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """Set a value in cache with TTL (default 5 minutes)."""
    expiry = time.time() + ttl_seconds
    _cache[key] = (value, expiry)


def delete_cached(key: str) -> None:
    """Delete a value from cache."""
    if key in _cache:
        del _cache[key]


def delete_pattern(pattern: str) -> int:
    """Delete all keys matching a pattern (e.g., 'movies:*')."""
    prefix = pattern.rstrip('*')
    keys_to_delete = [k for k in _cache.keys() if k.startswith(prefix)]
    for key in keys_to_delete:
        del _cache[key]
    return len(keys_to_delete)


def cache_result(key_template: str, ttl_seconds: int = 300):
    """
    Decorator to cache function results.
    Use {arg_name} in key_template to interpolate arguments.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key from template
            key = key_template
            # Simple interpolation for common patterns
            for i, arg in enumerate(args):
                key = key.replace(f'{{arg{i}}}', str(arg))
            for k, v in kwargs.items():
                key = key.replace(f'{{{k}}}', str(v))

            # Check cache
            cached = get_cached(key)
            if cached is not None:
                return cached

            # Execute and cache
            result = await func(*args, **kwargs)
            set_cached(key, result, ttl_seconds)
            return result
        return wrapper
    return decorator


def invalidate_movie_cache(movie_id: Optional[int] = None) -> int:
    """Invalidate all movie-related cache entries."""
    count = 0
    if movie_id:
        # Invalidate specific movie
        count += delete_pattern(f'movies:detail:{movie_id}')
    # Always invalidate movie lists
    count += delete_pattern('movies:list:')
    count += delete_pattern('movies:recommendations:')
    return count
