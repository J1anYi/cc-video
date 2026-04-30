"""Zero Trust Middleware for Request Interception"""
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from ..security.zero_trust import TrustLevel

logger = logging.getLogger(__name__)


class ZeroTrustMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces zero trust principles on every request
    """
    
    def __init__(
        self,
        app,
        zero_trust_engine=None,
        public_paths: list = None,
        high_trust_paths: list = None
    ):
        super().__init__(app)
        self.zero_trust = zero_trust_engine
        self.public_paths = public_paths or ["/health", "/metrics", "/docs", "/openapi.json"]
        self.high_trust_paths = high_trust_paths or ["/admin", "/config", "/secrets"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through zero trust verification"""
        
        # Skip public paths
        if request.url.path in self.public_paths:
            return await call_next(request)
        
        # Check for high-trust paths
        requires_high_trust = any(
            request.url.path.startswith(path) for path in self.high_trust_paths
        )
        
        # Get identity from headers
        user_id = request.headers.get("X-User-ID")
        session_id = request.headers.get("X-Session-ID")
        device_id = request.headers.get("X-Device-ID")
        
        # If no identity and not public path, require authentication
        if not user_id:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required"}
            )
        
        # Evaluate trust if zero trust engine available
        if self.zero_trust:
            from ..security.zero_trust import TrustContext
            
            context = TrustContext(
                user_id=int(user_id),
                device_id=device_id,
                session_id=session_id,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("User-Agent")
            )
            
            trust_level = await self.zero_trust.evaluate_trust(context)
            
            # Check if high trust required
            if requires_high_trust and trust_level.value < TrustLevel.HIGH.value:
                from fastapi.responses import JSONResponse
                return JSONResponse(
                    status_code=403,
                    content={
                        "detail": "Insufficient trust level for this resource",
                        "required_trust": "HIGH",
                        "current_trust": trust_level.name
                    }
                )
            
            # Add trust level to request state
            request.state.trust_level = trust_level
            request.state.trust_context = context
        
        return await call_next(request)
