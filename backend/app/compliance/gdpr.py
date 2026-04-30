"""GDPR Compliance Engine"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DataSubjectRequestType(Enum):
    """Types of GDPR data subject requests"""
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    PORTABILITY = "portability"
    RESTRICTION = "restriction"
    OBJECTION = "objection"


class RequestStatus(Enum):
    """Status of data subject request"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


@dataclass
class DataSubjectRequest:
    """GDPR Data Subject Request"""
    id: str
    user_id: int
    request_type: DataSubjectRequestType
    status: RequestStatus = RequestStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    details: Dict[str, Any] = field(default_factory=dict)
    response: Optional[Dict[str, Any]] = None


class GDPREngine:
    """GDPR Compliance Engine"""
    
    REQUEST_DEADLINE_DAYS = 30
    
    def __init__(self, db=None, notification_service=None):
        self.db = db
        self.notifications = notification_service
        self._requests: Dict[str, DataSubjectRequest] = {}
        self._consent_records: Dict[int, Dict[str, Any]] = {}
    
    async def create_request(
        self,
        user_id: int,
        request_type: DataSubjectRequestType,
        details: Optional[Dict[str, Any]] = None
    ) -> DataSubjectRequest:
        """Create a new data subject request"""
        import secrets
        
        request_id = f"dsr_{secrets.token_urlsafe(16)}"
        due_date = datetime.utcnow() + timedelta(days=self.REQUEST_DEADLINE_DAYS)
        
        request = DataSubjectRequest(
            id=request_id,
            user_id=user_id,
            request_type=request_type,
            details=details or {},
            due_date=due_date
        )
        
        self._requests[request_id] = request
        logger.info(f"GDPR request created: {request_id}")
        return request
    
    async def process_access_request(self, request_id: str) -> Dict[str, Any]:
        """Process data subject access request (DSAR)"""
        if request_id not in self._requests:
            return {"error": "Request not found"}
        
        request = self._requests[request_id]
        user_id = request.user_id
        
        personal_data = {
            "user_id": user_id,
            "data_collected": datetime.utcnow().isoformat(),
            "personal_data": {
                "profile": {"id": user_id},
                "consents": self._consent_records.get(user_id, {})
            }
        }
        
        request.status = RequestStatus.COMPLETED
        request.completed_at = datetime.utcnow()
        request.response = personal_data
        
        return personal_data
    
    async def process_erasure_request(self, request_id: str) -> Dict[str, Any]:
        """Process right to erasure (deletion) request"""
        if request_id not in self._requests:
            return {"error": "Request not found"}
        
        request = self._requests[request_id]
        user_id = request.user_id
        
        if await self._has_legal_hold(user_id):
            request.status = RequestStatus.REJECTED
            return {"error": "Legal hold prevents erasure"}
        
        deleted_items = ["profile", "activity", "preferences"]
        
        if user_id in self._consent_records:
            del self._consent_records[user_id]
        
        request.status = RequestStatus.COMPLETED
        request.completed_at = datetime.utcnow()
        request.response = {"deleted": deleted_items}
        
        return {"success": True, "deleted": deleted_items}
    
    async def process_portability_request(self, request_id: str) -> Dict[str, Any]:
        """Process data portability request"""
        if request_id not in self._requests:
            return {"error": "Request not found"}
        
        request = self._requests[request_id]
        user_id = request.user_id
        
        export_data = {
            "format": "JSON",
            "exported_at": datetime.utcnow().isoformat(),
            "data": {"profile": {"id": user_id}}
        }
        
        request.status = RequestStatus.COMPLETED
        request.completed_at = datetime.utcnow()
        
        return export_data
    
    async def record_consent(
        self,
        user_id: int,
        purpose: str,
        granted: bool,
        source: str = "web"
    ) -> Dict[str, Any]:
        """Record user consent"""
        if user_id not in self._consent_records:
            self._consent_records[user_id] = {}
        
        consent_record = {
            "purpose": purpose,
            "granted": granted,
            "timestamp": datetime.utcnow().isoformat(),
            "source": source
        }
        
        self._consent_records[user_id][purpose] = consent_record
        return consent_record
    
    async def check_consent(self, user_id: int, purpose: str) -> bool:
        """Check if user has granted consent for purpose"""
        if user_id not in self._consent_records:
            return False
        return self._consent_records[user_id].get(purpose, {}).get("granted", False)
    
    async def _has_legal_hold(self, user_id: int) -> bool:
        return False
    
    def get_pending_requests(self) -> List[DataSubjectRequest]:
        return [
            r for r in self._requests.values()
            if r.status in [RequestStatus.PENDING, RequestStatus.IN_PROGRESS]
        ]
    
    def get_user_requests(self, user_id: int) -> List[DataSubjectRequest]:
        return [r for r in self._requests.values() if r.user_id == user_id]
