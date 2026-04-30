"""Content workflow models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Text
from app.database import Base


class ContentApproval(Base):
    __tablename__ = "content_approvals"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending")
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentVersion(Base):
    __tablename__ = "content_versions"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    version = Column(Integer, default=1)
    data = Column(JSON, default=dict)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class QualityCheck(Base):
    __tablename__ = "quality_checks"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    check_type = Column(String(100), nullable=False)
    status = Column(String(50), default="pending")
    result = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentLifecycle(Base):
    __tablename__ = "content_lifecycles"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    status = Column(String(50), default="draft")
    transition_history = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.utcnow)


class BulkOperation(Base):
    __tablename__ = "bulk_operations"
    id = Column(Integer, primary_key=True, index=True)
    operation_type = Column(String(100), nullable=False)
    content_ids = Column(JSON, default=list)
    status = Column(String(50), default="pending")
    result = Column(JSON, default=dict)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
