"""Content workflow routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.content_workflow import ContentApproval, ContentVersion, QualityCheck, ContentLifecycle, BulkOperation

router = APIRouter(prefix="/workflow", tags=["content-workflow"])

@router.post("/approvals")
def create_approval(content_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    approval = ContentApproval(content_id=content_id, approver_id=current_user.id)
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

@router.get("/approvals/{content_id}")
def get_approvals(content_id: int, db: Session = Depends(get_db)):
    return db.query(ContentApproval).filter(ContentApproval.content_id == content_id).all()

@router.post("/versions")
def create_version(content_id: int, data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    version = ContentVersion(content_id=content_id, data=data, created_by=current_user.id)
    db.add(version)
    db.commit()
    db.refresh(version)
    return version

@router.get("/versions/{content_id}")
def get_versions(content_id: int, db: Session = Depends(get_db)):
    return db.query(ContentVersion).filter(ContentVersion.content_id == content_id).all()

@router.post("/quality-checks")
def run_quality_check(content_id: int, check_type: str, db: Session = Depends(get_db)):
    check = QualityCheck(content_id=content_id, check_type=check_type, status="passed")
    db.add(check)
    db.commit()
    db.refresh(check)
    return check

@router.get("/quality-checks/{content_id}")
def get_quality_checks(content_id: int, db: Session = Depends(get_db)):
    return db.query(QualityCheck).filter(QualityCheck.content_id == content_id).all()

@router.post("/lifecycle")
def update_lifecycle(content_id: int, status: str, db: Session = Depends(get_db)):
    lifecycle = ContentLifecycle(content_id=content_id, status=status)
    db.add(lifecycle)
    db.commit()
    db.refresh(lifecycle)
    return lifecycle

@router.post("/bulk")
def bulk_operation(operation_type: str, content_ids: List[int], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    operation = BulkOperation(operation_type=operation_type, content_ids=content_ids, created_by=current_user.id)
    db.add(operation)
    db.commit()
    db.refresh(operation)
    return operation
