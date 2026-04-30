"""Rights and licensing routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.rights import ContentRights, License, Royalty, RightsConflict, LicenseListing

router = APIRouter(prefix="/rights", tags=["rights"])

@router.post("/rights")
def create_rights(content_id: int, rights_type: str, db: Session = Depends(get_db)):
    rights = ContentRights(content_id=content_id, rights_type=rights_type)
    db.add(rights)
    db.commit()
    db.refresh(rights)
    return rights

@router.get("/rights/{content_id}")
def get_rights(content_id: int, db: Session = Depends(get_db)):
    return db.query(ContentRights).filter(ContentRights.content_id == content_id).all()

@router.post("/licenses")
def create_license(content_id: int, licensee_id: int, license_type: str, fee: float, db: Session = Depends(get_db)):
    license = License(content_id=content_id, licensee_id=licensee_id, license_type=license_type, fee=fee)
    db.add(license)
    db.commit()
    db.refresh(license)
    return license

@router.get("/licenses/{content_id}")
def get_licenses(content_id: int, db: Session = Depends(get_db)):
    return db.query(License).filter(License.content_id == content_id).all()

@router.post("/royalties")
def create_royalty(content_id: int, creator_id: int, period: str, views: int, revenue: float, db: Session = Depends(get_db)):
    royalty = Royalty(content_id=content_id, creator_id=creator_id, period=period, views=views, revenue=revenue, amount=revenue * 0.1)
    db.add(royalty)
    db.commit()
    db.refresh(royalty)
    return royalty

@router.get("/royalties/{creator_id}")
def get_royalties(creator_id: int, db: Session = Depends(get_db)):
    return db.query(Royalty).filter(Royalty.creator_id == creator_id).all()

@router.post("/conflicts")
def report_conflict(content_id: int, conflict_type: str, description: str, db: Session = Depends(get_db)):
    conflict = RightsConflict(content_id=content_id, conflict_type=conflict_type, description=description)
    db.add(conflict)
    db.commit()
    db.refresh(conflict)
    return conflict

@router.post("/marketplace")
def create_listing(content_id: int, title: str, price: float, db: Session = Depends(get_db)):
    listing = LicenseListing(content_id=content_id, title=title, price=price)
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

@router.get("/marketplace")
def get_listings(db: Session = Depends(get_db)):
    return db.query(LicenseListing).filter(LicenseListing.is_active == True).all()
