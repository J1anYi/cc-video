"""Identity-Aware Proxy for Zero Trust Access Control"""
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from functools import wraps
import logging

from fastapi import Request, HTTPException

logger = logging.getLogger(__name__)


class IdentityAwareProxy:
    """Identity-Aware Proxy (IAP) for endpoint protection"""
    
    def __init__(self, zero_trust_engine=None, trust_verifier=None):
        self.zero_trust = zero_trust_engine
        self.trust_verifier = trust_verifier
        self._protected_endpoints: Dict[str, Dict[str, Any]] = {}
    
    def protect_endpoint(
        self,
        required_trust_level: str = "MEDIUM",
        required_roles: Optional[list] = None
    ) -> Callable:
        """Decorator to protect endpoints with IAP"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = None
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                
                if not request:
                    request = kwargs.get("request")
                
                if request:
                    identity = await self._verify_identity(request)
                    trust_level = identity.get("trust_level", "NONE")
                    
                    if not self._check_trust_level(trust_level, required_trust_level):
                        raise HTTPException(
                            status_code=403,
                            detail="Insufficient trust level"
                        )
                    
                    if required_roles:
                        user_roles = identity.get("roles", [])
                        if not any(role in user_roles for role in required_roles):
                            raise HTTPException(
                                status_code=403,
                                detail="Insufficient permissions"
                            )
                    
                    kwargs["identity"] = identity
                
                return await func(*args, **kwargs)
            return wrapper
        return decorator
    
    async def _verify_identity(self, request: Request) -> Dict[str, Any]:
        """Verify identity from request headers and tokens"""
        identity = {
            "user_id": None,
            "email": None,
            "roles": [],
            "trust_level": "NONE",
            "device_id": None,
            "session_id": None
        }
        
        identity["user_id"] = request.headers.get("X-User-ID")
        identity["email"] = request.headers.get("X-User-Email")
        identity["device_id"] = request.headers.get("X-Device-ID")
        identity["session_id"] = request.headers.get("X-Session-ID")
        
        roles_header = request.headers.get("X-User-Roles", "")
        if roles_header:
            identity["roles"] = [r.strip() for r in roles_header.split(",")]
        
        identity["trust_level"] = request.headers.get("X-Trust-Level", "LOW")
        
        if self.zero_trust and identity["user_id"]:
            from .zero_trust import TrustContext
            context = TrustContext(
                user_id=int(identity["user_id"]),
                device_id=identity["device_id"],
                session_id=identity["session_id"],
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("User-Agent")
            )
            trust_level = await self.zero_trust.evaluate_trust(context)
            identity["trust_level"] = trust_level.name
        
        return identity
    
    def _check_trust_level(self, current: str, required: str) -> bool:
        """Check if current trust level meets requirement"""
        levels = ["NONE", "LOW", "MEDIUM", "HIGH", "FULL"]
        try:
            current_idx = levels.index(current)
            required_idx = levels.index(required)
            return current_idx >= required_idx
        except ValueError:
            return False
    
    def inject_identity_headers(
        self,
        headers: Dict[str, str],
        user_id: int,
        email: str,
        roles: list,
        trust_level: str = "MEDIUM",
        device_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, str]:
        """Inject identity headers for inter-service communication"""
        headers["X-User-ID"] = str(user_id)
        headers["X-User-Email"] = email
        headers["X-User-Roles"] = ",".join(roles)
        headers["X-Trust-Level"] = trust_level
        
        if device_id:
            headers["X-Device-ID"] = device_id
        if session_id:
            headers["X-Session-ID"] = session_id
        
        headers["X-Identity-Timestamp"] = datetime.utcnow().isoformat()
        
        return headers
    
    def register_endpoint(
        self,
        path: str,
        methods: list,
        required_trust: str = "MEDIUM",
        required_roles: Optional[list] = None
    ) -> None:
        """Register endpoint protection configuration"""
        self._protected_endpoints[path] = {
            "methods": methods,
            "required_trust": required_trust,
            "required_roles": required_roles or []
        }
    
    def get_protected_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """Get all protected endpoints"""
        return self._protected_endpoints.copy()
