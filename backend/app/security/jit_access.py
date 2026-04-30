"""Just-in-Time Access Provisioning"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import secrets
import logging

logger = logging.getLogger(__name__)


class AccessRequestStatus(Enum):
    """Status of access request"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class AccessRequest:
    """Access request for JIT provisioning"""
    id: str
    user_id: int
    resource: str
    permissions: List[str]
    reason: str
    duration_minutes: int
    status: AccessRequestStatus = AccessRequestStatus.PENDING
    requested_at: datetime = field(default_factory=datetime.utcnow)
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    token: Optional[str] = None


class JITAccessManager:
    """Just-in-Time Access Provisioning"""
    
    def __init__(self, db=None, notification_service=None):
        self.db = db
        self.notifications = notification_service
        self._requests: Dict[str, AccessRequest] = {}
        self._active_tokens: Dict[str, AccessRequest] = {}
        self._approvers: Dict[str, List[int]] = {
            "admin": [],
            "sensitive": [],
            "system": []
        }
    
    async def request_access(
        self,
        user_id: int,
        resource: str,
        permissions: List[str],
        reason: str,
        duration_minutes: int = 60,
        max_duration: int = 480
    ) -> AccessRequest:
        """Request time-bound access to a resource"""
        duration_minutes = min(duration_minutes, max_duration)
        
        request_id = secrets.token_urlsafe(16)
        request = AccessRequest(
            id=request_id,
            user_id=user_id,
            resource=resource,
            permissions=permissions,
            reason=reason,
            duration_minutes=duration_minutes
        )
        
        self._requests[request_id] = request
        
        if await self._can_auto_approve(user_id, resource, permissions):
            await self.approve_access(request_id, user_id)
        else:
            await self._notify_approvers(request)
        
        logger.info(f"Access request created: {request_id} by user {user_id}")
        return request
    
    async def approve_access(
        self,
        request_id: str,
        approver_id: int
    ) -> Optional[AccessRequest]:
        """Approve an access request"""
        if request_id not in self._requests:
            return None
        
        request = self._requests[request_id]
        
        if request.status != AccessRequestStatus.PENDING:
            return request
        
        request.status = AccessRequestStatus.APPROVED
        request.approved_by = approver_id
        request.approved_at = datetime.utcnow()
        request.expires_at = datetime.utcnow() + timedelta(
            minutes=request.duration_minutes
        )
        
        request.token = self._generate_access_token()
        self._active_tokens[request.token] = request
        
        logger.info(f"Access request approved: {request_id} by {approver_id}")
        return request
    
    async def reject_access(
        self,
        request_id: str,
        approver_id: int,
        reason: Optional[str] = None
    ) -> Optional[AccessRequest]:
        """Reject an access request"""
        if request_id not in self._requests:
            return None
        
        request = self._requests[request_id]
        
        if request.status != AccessRequestStatus.PENDING:
            return request
        
        request.status = AccessRequestStatus.REJECTED
        request.approved_by = approver_id
        request.approved_at = datetime.utcnow()
        
        logger.info(f"Access request rejected: {request_id} by {approver_id}")
        return request
    
    async def verify_access(
        self,
        token: str,
        resource: str,
        permission: str
    ) -> bool:
        """Verify if a token grants access to resource"""
        if token not in self._active_tokens:
            return False
        
        request = self._active_tokens[token]
        
        if request.expires_at and datetime.utcnow() > request.expires_at:
            await self.revoke_access(token)
            return False
        
        if request.resource != resource:
            return False
        
        if permission not in request.permissions:
            return False
        
        return True
    
    async def revoke_access(self, token: str) -> bool:
        """Revoke an active access token"""
        if token not in self._active_tokens:
            return False
        
        request = self._active_tokens[token]
        request.status = AccessRequestStatus.REVOKED
        del self._active_tokens[token]
        
        logger.info(f"Access revoked: {request.id}")
        return True
    
    def _generate_access_token(self) -> str:
        """Generate a secure access token"""
        return f"jit_{secrets.token_urlsafe(32)}"
    
    async def _can_auto_approve(
        self,
        user_id: int,
        resource: str,
        permissions: List[str]
    ) -> bool:
        """Check if request can be auto-approved"""
        safe_permissions = {"read", "list", "view"}
        if all(p in safe_permissions for p in permissions):
            sensitive_patterns = ["admin", "config", "secret", "key"]
            if not any(p in resource.lower() for p in sensitive_patterns):
                return True
        return False
    
    async def _notify_approvers(self, request: AccessRequest) -> None:
        """Notify approvers of pending request"""
        if self.notifications:
            await self.notifications.send(
                channel="access-requests",
                message={
                    "type": "access_request",
                    "request_id": request.id,
                    "user_id": request.user_id,
                    "resource": request.resource
                }
            )
    
    def get_user_requests(
        self,
        user_id: int,
        status: Optional[AccessRequestStatus] = None
    ) -> List[AccessRequest]:
        """Get all requests for a user"""
        requests = [r for r in self._requests.values() if r.user_id == user_id]
        if status:
            requests = [r for r in requests if r.status == status]
        return sorted(requests, key=lambda r: r.requested_at, reverse=True)
    
    def get_pending_requests(self) -> List[AccessRequest]:
        """Get all pending requests"""
        return [r for r in self._requests.values() if r.status == AccessRequestStatus.PENDING]
    
    async def cleanup_expired(self) -> int:
        """Remove expired requests and tokens"""
        now = datetime.utcnow()
        expired_count = 0
        
        for token, request in list(self._active_tokens.items()):
            if request.expires_at and now > request.expires_at:
                request.status = AccessRequestStatus.EXPIRED
                del self._active_tokens[token]
                expired_count += 1
        
        return expired_count
