from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class APIVersion:
    V1 = "v1"
    V2 = "v2"
    CURRENT = V1


DEPRECATED_ENDPOINTS: Dict[str, Dict[str, Any]] = {}
SUNSET_DATES: Dict[str, datetime] = {}


class VersioningMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, default_version: str = APIVersion.CURRENT):
        super().__init__(app)
        self.default_version = default_version

    async def dispatch(self, request: Request, call_next):
        # Extract version from path or header
        version = self._extract_version(request)
        request.state.api_version = version

        # Process request
        response = await call_next(request)

        # Add version headers
        response.headers["X-API-Version"] = version
        response.headers["X-API-Supported-Versions"] = "v1, v2"

        # Check for deprecation
        endpoint_key = f"{request.method}:{request.url.path}"
        if endpoint_key in DEPRECATED_ENDPOINTS:
            deprecation_info = DEPRECATED_ENDPOINTS[endpoint_key]
            response.headers["X-API-Deprecated"] = "true"
            response.headers["X-API-Deprecation-Message"] = deprecation_info.get("message", "")
            
            if endpoint_key in SUNSET_DATES:
                sunset_date = SUNSET_DATES[endpoint_key]
                response.headers["X-API-Sunset"] = sunset_date.isoformat()
                response.headers["Sunset"] = sunset_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return response

    def _extract_version(self, request: Request) -> str:
        # Check path prefix
        path = request.url.path
        if path.startswith("/v2/"):
            return APIVersion.V2
        elif path.startswith("/v1/"):
            return APIVersion.V1

        # Check header
        accept_version = request.headers.get("X-API-Version")
        if accept_version in [APIVersion.V1, APIVersion.V2]:
            return accept_version

        # Check Accept header
        accept = request.headers.get("Accept", "")
        if "application/vnd.api.v2+json" in accept:
            return APIVersion.V2

        return self.default_version


def deprecate_endpoint(
    method: str,
    path: str,
    message: str,
    sunset_days: int = 180,
    migration_path: Optional[str] = None,
):
    """Mark an endpoint as deprecated."""
    endpoint_key = f"{method}:{path}"
    DEPRECATED_ENDPOINTS[endpoint_key] = {
        "message": message,
        "migration_path": migration_path,
        "deprecated_at": datetime.utcnow().isoformat(),
    }
    SUNSET_DATES[endpoint_key] = datetime.utcnow() + timedelta(days=sunset_days)
    logger.info(f"Deprecated endpoint: {endpoint_key} - {message}")


def get_deprecated_endpoints() -> Dict[str, Dict[str, Any]]:
    """Get all deprecated endpoints."""
    result = {}
    for key, info in DEPRECATED_ENDPOINTS.items():
        result[key] = {
            **info,
            "sunset_date": SUNSET_DATES.get(key).isoformat() if key in SUNSET_DATES else None,
        }
    return result
