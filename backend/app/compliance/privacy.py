"""Privacy Impact Assessment Engine"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AssessmentStatus(Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class RiskAssessment:
    category: str
    description: str
    likelihood: int  # 1-5
    impact: int  # 1-5
    mitigation: Optional[str] = None
    residual_risk: Optional[str] = None


@dataclass
class PrivacyImpactAssessment:
    id: str
    name: str
    description: str
    data_types: List[str]
    status: AssessmentStatus = AssessmentStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    risk_assessments: List[RiskAssessment] = field(default_factory=list)
    overall_risk: Optional[RiskLevel] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None


class PrivacyAssessmentEngine:
    def __init__(self):
        self._assessments: Dict[str, PrivacyImpactAssessment] = {}
        self._risk_thresholds = {
            RiskLevel.LOW: 4,
            RiskLevel.MEDIUM: 8,
            RiskLevel.HIGH: 12,
            RiskLevel.CRITICAL: 16
        }
    
    async def create_assessment(
        self,
        name: str,
        description: str,
        data_types: List[str]
    ) -> PrivacyImpactAssessment:
        import secrets
        
        assessment = PrivacyImpactAssessment(
            id=f"pia_{secrets.token_urlsafe(8)}",
            name=name,
            description=description,
            data_types=data_types
        )
        
        self._assessments[assessment.id] = assessment
        logger.info(f"PIA created: {assessment.id} name={name}")
        return assessment
    
    async def add_risk_assessment(
        self,
        assessment_id: str,
        category: str,
        description: str,
        likelihood: int,
        impact: int,
        mitigation: Optional[str] = None
    ) -> RiskAssessment:
        if assessment_id not in self._assessments:
            raise ValueError("Assessment not found")
        
        if not 1 <= likelihood <= 5 or not 1 <= impact <= 5:
            raise ValueError("Likelihood and impact must be 1-5")
        
        risk = RiskAssessment(
            category=category,
            description=description,
            likelihood=likelihood,
            impact=impact,
            mitigation=mitigation
        )
        
        assessment = self._assessments[assessment_id]
        assessment.risk_assessments.append(risk)
        assessment.updated_at = datetime.utcnow()
        
        # Recalculate overall risk
        assessment.overall_risk = self._calculate_overall_risk(assessment)
        
        return risk
    
    def _calculate_overall_risk(
        self,
        assessment: PrivacyImpactAssessment
    ) -> RiskLevel:
        if not assessment.risk_assessments:
            return RiskLevel.LOW
        
        max_risk_score = 0
        for risk in assessment.risk_assessments:
            score = risk.likelihood * risk.impact
            max_risk_score = max(max_risk_score, score)
        
        for level, threshold in [
            (RiskLevel.CRITICAL, self._risk_thresholds[RiskLevel.CRITICAL]),
            (RiskLevel.HIGH, self._risk_thresholds[RiskLevel.HIGH]),
            (RiskLevel.MEDIUM, self._risk_thresholds[RiskLevel.MEDIUM]),
        ]:
            if max_risk_score >= threshold:
                return level
        
        return RiskLevel.LOW
    
    async def submit_for_review(
        self,
        assessment_id: str
    ) -> Dict[str, Any]:
        if assessment_id not in self._assessments:
            return {"error": "Assessment not found"}
        
        assessment = self._assessments[assessment_id]
        
        if not assessment.risk_assessments:
            return {"error": "Must add at least one risk assessment"}
        
        assessment.status = AssessmentStatus.IN_REVIEW
        assessment.updated_at = datetime.utcnow()
        
        return {
            "assessment_id": assessment_id,
            "status": assessment.status.value,
            "overall_risk": assessment.overall_risk.value if assessment.overall_risk else None
        }
    
    async def approve_assessment(
        self,
        assessment_id: str,
        approver_id: int
    ) -> Dict[str, Any]:
        if assessment_id not in self._assessments:
            return {"error": "Assessment not found"}
        
        assessment = self._assessments[assessment_id]
        
        if assessment.status != AssessmentStatus.IN_REVIEW:
            return {"error": "Assessment must be in review"}
        
        # Check if high risk requires additional approval
        if assessment.overall_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            logger.warning(
                f"Approving high-risk PIA: {assessment_id} risk={assessment.overall_risk.value}"
            )
        
        assessment.status = AssessmentStatus.APPROVED
        assessment.approved_by = approver_id
        assessment.approved_at = datetime.utcnow()
        assessment.updated_at = datetime.utcnow()
        
        return {
            "assessment_id": assessment_id,
            "status": assessment.status.value,
            "approved_by": approver_id,
            "approved_at": assessment.approved_at.isoformat()
        }
    
    async def reject_assessment(
        self,
        assessment_id: str,
        reason: str
    ) -> Dict[str, Any]:
        if assessment_id not in self._assessments:
            return {"error": "Assessment not found"}
        
        assessment = self._assessments[assessment_id]
        assessment.status = AssessmentStatus.REJECTED
        assessment.updated_at = datetime.utcnow()
        
        return {
            "assessment_id": assessment_id,
            "status": assessment.status.value,
            "reason": reason
        }
    
    def get_assessment(self, assessment_id: str) -> Optional[PrivacyImpactAssessment]:
        return self._assessments.get(assessment_id)
    
    def list_assessments(
        self,
        status: Optional[AssessmentStatus] = None
    ) -> List[PrivacyImpactAssessment]:
        assessments = list(self._assessments.values())
        
        if status:
            assessments = [a for a in assessments if a.status == status]
        
        return sorted(assessments, key=lambda a: a.created_at, reverse=True)
    
    async def get_risk_summary(self) -> Dict[str, Any]:
        summary = {
            RiskLevel.LOW.value: 0,
            RiskLevel.MEDIUM.value: 0,
            RiskLevel.HIGH.value: 0,
            RiskLevel.CRITICAL.value: 0
        }
        
        for assessment in self._assessments.values():
            if assessment.overall_risk:
                summary[assessment.overall_risk.value] += 1
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "total_assessments": len(self._assessments),
            "by_risk_level": summary
        }
