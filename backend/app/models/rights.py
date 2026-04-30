"""Rights and licensing models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Text, Float
from app.database import Base


class ContentRights(Base):
    __tablename__ = "content_rights"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    rights_type = Column(String(100), nullable=False)
    territory = Column(String(100), default="worldwide")
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    exclusive = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentLicense(Base):
    """Content license for rights management (separate from marketplace License)."""
    __tablename__ = "content_licenses"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    licensee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    license_type = Column(String(100), nullable=False)
    fee = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class Royalty(Base):
    __tablename__ = "royalties"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("creator_profiles.id"), nullable=False)
    period = Column(String(20), nullable=False)
    views = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    royalty_rate = Column(Float, default=0.0)
    amount = Column(Float, default=0.0)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


class RightsConflict(Base):
    __tablename__ = "rights_conflicts"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    conflict_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="open")
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class LicenseListing(Base):
    __tablename__ = "license_listings"
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("creator_contents.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, default=0.0)
    license_type = Column(String(100), default="standard")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
