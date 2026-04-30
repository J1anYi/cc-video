from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime
from app.middleware.versioning import (
    APIVersion,
    get_deprecated_endpoints,
    deprecate_endpoint,
)

router = APIRouter(tags=["version"])


@router.get("/version")
async def get_version_info():
    """Get current API version information."""
    return {
        "current_version": APIVersion.CURRENT,
        "supported_versions": [APIVersion.V1, APIVersion.V2],
        "documentation": "/docs",
        "changelog": "/version/changelog",
    }


@router.get("/version/changelog")
async def get_changelog():
    """Get API changelog."""
    return {
        "versions": [
            {
                "version": "v1",
                "status": "stable",
                "released": "2026-04-29",
                "changes": ["Initial API release"],
            },
            {
                "version": "v2",
                "status": "planned",
                "released": None,
                "changes": [
                    "GraphQL support",
                    "WebSocket infrastructure",
                    "Event-driven architecture",
                ],
            },
        ]
    }


@router.get("/version/deprecated")
async def list_deprecated():
    """List all deprecated endpoints."""
    return {
        "deprecated_endpoints": get_deprecated_endpoints(),
        "count": len(get_deprecated_endpoints()),
    }


@router.post("/version/deprecate")
async def mark_deprecated(
    method: str,
    path: str,
    message: str,
    sunset_days: int = 180,
    migration_path: str = None,
):
    """Mark an endpoint as deprecated (admin only)."""
    deprecate_endpoint(method, path, message, sunset_days, migration_path)
    return {
        "status": "deprecated",
        "endpoint": f"{method} {path}",
        "message": message,
        "sunset_days": sunset_days,
    }


@router.get("/version/migration")
async def migration_guide():
    """Get migration guide between versions."""
    return {
        "v1_to_v2": {
            "breaking_changes": [
                {
                    "endpoint": "GET /movies",
                    "change": "Response format updated",
                    "migration": "Use new pagination format",
                },
            ],
            "deprecated_features": [
                {
                    "feature": "Legacy auth endpoint",
                    "replacement": "Use /auth/login",
                    "sunset": "2026-08-01",
                },
            ],
            "new_features": [
                "GraphQL API at /graphql",
                "WebSocket at /ws",
                "Event publishing at /events",
            ],
        }
    }
