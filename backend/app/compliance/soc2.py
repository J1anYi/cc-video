"""SOC 2 Compliance Controls"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ControlCategory(Enum):
    SECURITY = "security"
    AVAILABILITY = "availability"
    PROCESSING_INTEGRITY = "processing_integrity"
    CONFIDENTIALITY = "confidentiality"
    PRIVACY = "privacy"


class ControlStatus(Enum):
    NOT_IMPLEMENTED = "not_implemented"
    PARTIAL = "partial"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"


@dataclass
class AuditEvidence:
    id: str
    control_id: str
    evidence_type: str
    collected_at: datetime = field(default_factory=datetime.utcnow)
    description: str = ""
    file_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceControl:
    id: str
    name: str
    category: ControlCategory
    description: str
    status: ControlStatus = ControlStatus.NOT_IMPLEMENTED
    last_audit: Optional[datetime] = None
    evidence: List[AuditEvidence] = field(default_factory=list)


class SOC2Controls:
    def __init__(self):
        self._controls: Dict[str, ComplianceControl] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self._initialize_controls()
    
    def _initialize_controls(self):
        controls = [
            ("CC6.1", "Logical and Physical Access", ControlCategory.SECURITY),
            ("CC6.2", "System Account Management", ControlCategory.SECURITY),
            ("CC6.3", "Network Access Control", ControlCategory.SECURITY),
            ("CC6.6", "Security Incident Management", ControlCategory.SECURITY),
            ("CC7.1", "Vulnerability Management", ControlCategory.SECURITY),
            ("CC7.2", "Anomaly Detection", ControlCategory.SECURITY),
            ("A1.1", "System Availability", ControlCategory.AVAILABILITY),
            ("A1.2", "Disaster Recovery", ControlCategory.AVAILABILITY),
            ("PI1.1", "Data Processing Accuracy", ControlCategory.PROCESSING_INTEGRITY),
            ("C1.1", "Data Classification", ControlCategory.CONFIDENTIALITY),
            ("P1.1", "Privacy Policy", ControlCategory.PRIVACY),
            ("P2.1", "Consent Management", ControlCategory.PRIVACY),
        ]
        
        for control_id, name, category in controls:
            self._controls[control_id] = ComplianceControl(
                id=control_id,
                name=name,
                category=category,
                description=f"SOC 2 control: {name}"
            )
    
    async def assess_control(self, control_id: str) -> Dict[str, Any]:
        if control_id not in self._controls:
            return {"error": "Control not found"}
        
        control = self._controls[control_id]
        status = await self._evaluate_control(control)
        control.status = status
        
        return {
            "control_id": control_id,
            "name": control.name,
            "category": control.category.value,
            "status": status.value,
            "assessed_at": datetime.utcnow().isoformat()
        }
    
    async def _evaluate_control(self, control: ComplianceControl) -> ControlStatus:
        if control.id.startswith("CC6"):
            return ControlStatus.IMPLEMENTED
        elif control.id.startswith("CC7"):
            return ControlStatus.VERIFIED
        else:
            return ControlStatus.PARTIAL
    
    async def collect_evidence(
        self,
        control_id: str,
        evidence_type: str,
        description: str,
        file_path: Optional[str] = None
    ) -> AuditEvidence:
        import secrets
        
        if control_id not in self._controls:
            raise ValueError("Control not found")
        
        evidence = AuditEvidence(
            id=f"ev_{secrets.token_urlsafe(8)}",
            control_id=control_id,
            evidence_type=evidence_type,
            description=description,
            file_path=file_path
        )
        
        self._controls[control_id].evidence.append(evidence)
        logger.info(f"Evidence collected: {evidence.id} for {control_id}")
        return evidence
    
    async def generate_audit_report(
        self,
        categories: Optional[List[ControlCategory]] = None
    ) -> Dict[str, Any]:
        controls = []
        
        for control in self._controls.values():
            if categories and control.category not in categories:
                continue
            
            controls.append({
                "id": control.id,
                "name": control.name,
                "category": control.category.value,
                "status": control.status.value,
                "evidence_count": len(control.evidence)
            })
        
        implemented = sum(
            1 for c in self._controls.values()
            if c.status in [ControlStatus.IMPLEMENTED, ControlStatus.VERIFIED]
        )
        total = len(self._controls)
        compliance_score = implemented / total if total > 0 else 0
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "compliance_score": round(compliance_score * 100, 2),
            "total_controls": total,
            "implemented": implemented,
            "controls": controls
        }
    
    def get_controls_by_category(self, category: ControlCategory) -> List[ComplianceControl]:
        return [c for c in self._controls.values() if c.category == category]
    
    def log_audit_event(self, event_type: str, details: Dict[str, Any]) -> None:
        self._audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details
        })
    
    def get_audit_log(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        if since:
            return [
                e for e in self._audit_log
                if datetime.fromisoformat(e["timestamp"]) >= since
            ]
        return self._audit_log.copy()
