"""Rate limiting middleware for API endpoints."""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

from app.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware with IP-based and user-based limits.
    Uses in-memory storage (suitable for single instance).
    For multi-instance, replace with Redis-backed storage.
    """

    # Rate limit configuration
    PUBLIC_LIMITS = {
        "/api/auth/login": (5, 60),  # 5 requests per 60 seconds
        "/api/auth/register": (3, 60),  # 3 requests per 60 seconds
        "/api/auth/forgot-password": (3, 300),  # 3 requests per 5 minutes
    }

    DEFAULT_PUBLIC_LIMIT = (100, 60)  # 100 requests per minute for public endpoints
    AUTHENTICATED_LIMIT = (300, 60)  # 300 requests per minute for authenticated users
    ADMIN_LIMIT = (500, 60)  # 500 requests per minute for admin users

    def __init__(self, app):
        super().__init__(app)
        # In-memory rate limit storage: {key: [(timestamp, count), ...]}
        self._rate_limits: dict[str, list[float]] = defaultdict(list)

    def _get_client_key(self, request: Request) -> str:
        """Get unique identifier for the client."""
        # Try to get user ID from auth context
        user = getattr(request.state, "user", None)
        if user:
            return f"user:{user.get('id', 'unknown')}"

        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0].strip()}"
        return f"ip:{request.client.host if request.client else 'unknown'}"

    def _get_rate_limit(self, request: Request) -> tuple[int, int]:
        """Get rate limit (max_requests, window_seconds) for the request."""
        path = request.url.path

        # Check for specific endpoint limits
        if path in self.PUBLIC_LIMITS:
            return self.PUBLIC_LIMITS[path]

        # Check if user is authenticated
        user = getattr(request.state, "user", None)
        if user:
            if user.get("is_admin"):
                return self.ADMIN_LIMIT
            return self.AUTHENTICATED_LIMIT

        return self.DEFAULT_PUBLIC_LIMIT

    def _is_rate_limited(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, int]:
        """
        Check if the key is rate limited.
        Returns (is_limited, retry_after_seconds).
        """
        now = time.time()
        window_start = now - window_seconds

        # Clean old entries
        self._rate_limits[key] = [
            ts for ts in self._rate_limits[key] if ts > window_start
        ]

        # Check limit
        if len(self._rate_limits[key]) >= max_requests:
            oldest = min(self._rate_limits[key])
            retry_after = int(oldest + window_seconds - now) + 1
            return True, max(1, retry_after)

        # Record request
        self._rate_limits[key].append(now)
        return False, 0

    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/health", "/"] or request.url.path.startswith("/uploads/"):
            return await call_next(request)

        # Get rate limit for this request
        max_requests, window_seconds = self._get_rate_limit(request)

        # Get client identifier
        key = f"{self._get_client_key(request)}:{request.url.path}"

        # Check rate limit
        is_limited, retry_after = self._is_rate_limited(key, max_requests, window_seconds)

        if is_limited:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(retry_after)}
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        remaining = max(0, max_requests - len(self._rate_limits[key]))
        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + window_seconds))

        return response
