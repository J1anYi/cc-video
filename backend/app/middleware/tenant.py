from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.tenant import Tenant
from app.services.tenant_service import tenant_service


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = None
        tenant = None

        # 1. Try to get tenant from X-Tenant-ID header
        tenant_header = request.headers.get('X-Tenant-ID')
        if tenant_header:
            try:
                tenant_id = int(tenant_header)
            except ValueError:
                pass

        # 2. Try to get tenant from subdomain
        if not tenant_id:
            host = request.headers.get('host', '')
            parts = host.split('.')
            if len(parts) >= 2 and parts[0] not in ('www', 'api', 'localhost', '127'):
                subdomain = parts[0]
                async with AsyncSessionLocal() as db:
                    tenant = await tenant_service.get_by_slug(db, subdomain)
                    if tenant:
                        tenant_id = tenant.id

        # 3. Store tenant_id in request state
        request.state.tenant_id = tenant_id
        request.state.tenant = tenant

        response = await call_next(request)
        return response


def get_tenant_from_request(request: Request) -> Optional[int]:
    return getattr(request.state, 'tenant_id', None)
