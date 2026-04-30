"""Data Retention Policy Engine"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class RetentionAction(Enum):
    RETAIN = "retain"
    ARCHIVE = "archive"
    DELETE = "delete"
    REVIEW = "review"


@dataclass
class RetentionPolicy:
    name: str
    classification: DataClassification
    retention_days: int
    action: RetentionAction
    description: str = ""
    legal_basis: Optional[str] = None


@dataclass
class DataRecord:
    id: str
    data_type: str
    classification: DataClassification
    created_at: datetime
    last_accessed: Optional[datetime] = None
    size_bytes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataClassifier:
    def __init__(self):
        self._classification_rules: List[Dict[str, Any]] = []
    
    def classify(self, data: Dict[str, Any]) -> DataClassification:
        if self._contains_pii(data):
            return DataClassification.CONFIDENTIAL
        elif self._contains_sensitive(data):
            return DataClassification.RESTRICTED
        elif self._is_internal(data):
            return DataClassification.INTERNAL
        return DataClassification.PUBLIC
    
    def _contains_pii(self, data: Dict[str, Any]) -> bool:
        pii_fields = ["email", "phone", "ssn", "address", "name"]
        return any(k in data for k in pii_fields)
    
    def _contains_sensitive(self, data: Dict[str, Any]) -> bool:
        sensitive_fields = ["password", "credit_card", "api_key", "token"]
        return any(k in data for k in sensitive_fields)
    
    def _is_internal(self, data: Dict[str, Any]) -> bool:
        internal_fields = ["internal_id", "company_id", "department"]
        return any(k in data for k in internal_fields)


class RetentionPolicyEngine:
    def __init__(self):
        self._policies: Dict[str, RetentionPolicy] = {}
        self._data_records: Dict[str, DataRecord] = {}
        self._classifier = DataClassifier()
        self._initialize_policies()
    
    def _initialize_policies(self):
        policies = [
            RetentionPolicy(
                name="public_data",
                classification=DataClassification.PUBLIC,
                retention_days=365,
                action=RetentionAction.DELETE,
                description="Public data retained for 1 year"
            ),
            RetentionPolicy(
                name="internal_data",
                classification=DataClassification.INTERNAL,
                retention_days=730,
                action=RetentionAction.ARCHIVE,
                description="Internal data retained for 2 years"
            ),
            RetentionPolicy(
                name="confidential_data",
                classification=DataClassification.CONFIDENTIAL,
                retention_days=1095,
                action=RetentionAction.REVIEW,
                description="Confidential data retained for 3 years",
                legal_basis="GDPR Article 5(1)(e)"
            ),
            RetentionPolicy(
                name="restricted_data",
                classification=DataClassification.RESTRICTED,
                retention_days=2555,
                action=RetentionAction.REVIEW,
                description="Restricted data retained for 7 years",
                legal_basis="SOX 802"
            ),
        ]
        
        for policy in policies:
            self._policies[policy.name] = policy
    
    async def register_data(
        self,
        data_type: str,
        data: Dict[str, Any],
        user_id: Optional[int] = None
    ) -> DataRecord:
        import secrets
        
        classification = self._classifier.classify(data)
        
        record = DataRecord(
            id=f"rec_{secrets.token_urlsafe(8)}",
            data_type=data_type,
            classification=classification,
            created_at=datetime.utcnow(),
            metadata={"user_id": user_id}
        )
        
        self._data_records[record.id] = record
        logger.info(f"Data registered: {record.id} classification={classification.value}")
        return record
    
    async def get_retention_action(
        self,
        record_id: str
    ) -> Dict[str, Any]:
        if record_id not in self._data_records:
            return {"error": "Record not found"}
        
        record = self._data_records[record_id]
        policy = self._get_policy_for_classification(record.classification)
        
        age_days = (datetime.utcnow() - record.created_at).days
        remaining_days = policy.retention_days - age_days
        
        action = policy.action if remaining_days <= 0 else RetentionAction.RETAIN
        
        return {
            "record_id": record_id,
            "classification": record.classification.value,
            "policy": policy.name,
            "age_days": age_days,
            "retention_days": policy.retention_days,
            "remaining_days": max(0, remaining_days),
            "action": action.value,
            "legal_basis": policy.legal_basis
        }
    
    def _get_policy_for_classification(
        self,
        classification: DataClassification
    ) -> RetentionPolicy:
        for policy in self._policies.values():
            if policy.classification == classification:
                return policy
        return self._policies["public_data"]
    
    async def enforce_retention(self) -> Dict[str, Any]:
        actions_taken = {
            "archived": 0,
            "deleted": 0,
            "flagged_for_review": 0
        }
        
        for record_id, record in list(self._data_records.items()):
            retention_info = await self.get_retention_action(record_id)
            action = retention_info["action"]
            
            if action == RetentionAction.ARCHIVE.value:
                actions_taken["archived"] += 1
            elif action == RetentionAction.DELETE.value:
                del self._data_records[record_id]
                actions_taken["deleted"] += 1
            elif action == RetentionAction.REVIEW.value:
                actions_taken["flagged_for_review"] += 1
        
        logger.info(f"Retention enforcement: {actions_taken}")
        return actions_taken
    
    async def get_retention_report(self) -> Dict[str, Any]:
        total_records = len(self._data_records)
        
        by_classification = {}
        for classification in DataClassification:
            count = sum(
                1 for r in self._data_records.values()
                if r.classification == classification
            )
            by_classification[classification.value] = count
        
        pending_actions = {
            "archive": 0,
            "delete": 0,
            "review": 0
        }
        
        for record_id in self._data_records:
            info = await self.get_retention_action(record_id)
            action = info["action"]
            if action in pending_actions:
                pending_actions[action] += 1
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "total_records": total_records,
            "by_classification": by_classification,
            "pending_actions": pending_actions
        }
