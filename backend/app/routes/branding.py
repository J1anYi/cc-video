from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid

from app.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.branding import BrandingSettings, BrandingUpdate
from app.services.branding_service import branding_service
from app.config import settings


router = APIRouter(prefix="/branding", tags=["branding"])


@router.get("/", response_model=BrandingSettings)
async def get_branding(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BrandingSettings:
    if not current_user.tenant_id:
        return BrandingSettings()
    return await branding_service.get_branding(db, current_user.tenant_id)


@router.put("/", response_model=BrandingSettings)
async def update_branding(
    update: BrandingUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> BrandingSettings:
    if not admin.tenant_id:
        raise HTTPException(status_code=400, detail="No tenant context")
    return await branding_service.update_branding(db, admin.tenant_id, update)


@router.post("/logo", response_model=dict)
async def upload_logo(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> dict:
    if not admin.tenant_id:
        raise HTTPException(status_code=400, detail="No tenant context")
    
    ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    filename = f"{uuid.uuid4()}{ext}"
    logos_dir = os.path.join(settings.UPLOAD_DIR, "logos")
    os.makedirs(logos_dir, exist_ok=True)
    
    filepath = os.path.join(logos_dir, filename)
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    logo_url = f"/uploads/logos/{filename}"
    await branding_service.set_logo(db, admin.tenant_id, logo_url)
    
    return {"logo_url": logo_url}


@router.post("/favicon", response_model=dict)
async def upload_favicon(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
) -> dict:
    if not admin.tenant_id:
        raise HTTPException(status_code=400, detail="No tenant context")
    
    ext = os.path.splitext(file.filename)[1] if file.filename else ".ico"
    filename = f"{uuid.uuid4()}{ext}"
    favicons_dir = os.path.join(settings.UPLOAD_DIR, "favicons")
    os.makedirs(favicons_dir, exist_ok=True)
    
    filepath = os.path.join(favicons_dir, filename)
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    
    favicon_url = f"/uploads/favicons/{filename}"
    await branding_service.set_favicon(db, admin.tenant_id, favicon_url)
    
    return {"favicon_url": favicon_url}
