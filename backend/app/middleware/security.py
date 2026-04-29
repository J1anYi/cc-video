"""Security middleware for headers, HTTPS, and CSRF protection."""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import secrets
import hashlib
from typing import Callable

from app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security-related headers to all responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # unsafe-inline needed for React
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # XSS Protection (legacy but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # HTTP Strict Transport Security (HSTS)
        # Only enable in production with HTTPS
        if settings.DEBUG is False:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Permissions Policy (formerly Feature Policy)
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    """
    CSRF protection middleware.
    Generates and validates CSRF tokens for state-changing operations.
    """

    # Methods that require CSRF protection
    PROTECTED_METHODS = {"POST", "PUT", "DELETE", "PATCH"}

    # Paths exempt from CSRF (e.g., API endpoints with token auth)
    EXEMPT_PATHS = {
        "/health",
        "/healthz",
        "/readyz",
        "/docs",
        "/openapi.json",
    }

    # Token header name
    CSRF_HEADER = "X-CSRF-Token"
    CSRF_COOKIE = "csrf_token"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip CSRF for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        # Skip CSRF for safe methods
        if request.method not in self.PROTECTED_METHODS:
            response = await call_next(request)
            # Set CSRF token cookie on safe requests
            await self._set_csrf_cookie(request, response)
            return response

        # For protected methods, validate CSRF token
        csrf_token = request.headers.get(self.CSRF_HEADER)
        cookie_token = request.cookies.get(self.CSRF_COOKIE)

        if not csrf_token or not cookie_token:
            return JSONResponse(
                {"detail": "CSRF token missing"},
                status_code=403,
            )

        # Validate token
        if not self._validate_csrf_token(csrf_token, cookie_token):
            return JSONResponse(
                {"detail": "Invalid CSRF token"},
                status_code=403,
            )

        return await call_next(request)

    async def _set_csrf_cookie(self, request: Request, response: Response) -> None:
        """Set CSRF token cookie if not present."""
        if self.CSRF_COOKIE not in request.cookies:
            token = self._generate_csrf_token()
            response.set_cookie(
                key=self.CSRF_COOKIE,
                value=token,
                httponly=False,  # Must be accessible to JavaScript
                secure=not settings.DEBUG,
                samesite="strict",
            )

    def _generate_csrf_token(self) -> str:
        """Generate a secure CSRF token."""
        return secrets.token_urlsafe(32)

    def _validate_csrf_token(self, header_token: str, cookie_token: str) -> bool:
        """Validate CSRF token from header against cookie."""
        # Use constant-time comparison to prevent timing attacks
        return secrets.compare_digest(header_token, cookie_token)


class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Redirect HTTP requests to HTTPS in production."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip redirect in development
        if settings.DEBUG:
            return await call_next(request)

        # Check if request is already HTTPS
        if request.url.scheme == "https":
            return await call_next(request)

        # Check X-Forwarded-Proto header (for reverse proxies)
        forwarded_proto = request.headers.get("X-Forwarded-Proto", "")
        if forwarded_proto == "https":
            return await call_next(request)

        # Redirect to HTTPS
        https_url = request.url.replace(scheme="https")
        return Response(
            status_code=301,
            headers={"Location": str(https_url)},
        )


def sanitize_html(text: str) -> str:
    """
    Sanitize HTML to prevent XSS.
    Removes dangerous tags and attributes.
    """
    import html
    # Escape HTML entities
    return html.escape(text)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets security requirements.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password must be less than 128 characters"

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not (has_lower and has_upper and has_digit):
        return False, "Password must contain uppercase, lowercase, and numbers"

    return True, ""
