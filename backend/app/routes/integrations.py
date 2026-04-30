"""Third-party integrations routes."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.dependencies import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.middleware.tenant import get_tenant_id
from app.models.integration import OAuthConnection, WebhookConfig, WebhookDelivery

router = APIRouter(prefix="/integrations", tags=["integrations"])

class WebhookCreate(BaseModel):
    name: str
    url: str
    events: Optional[str] = None
    secret: Optional[str] = None

class OAuthConnect(BaseModel):
    provider: str
    code: str

@router.get("/oauth")
async def get_oauth_connections(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    from sqlalchemy import select
    query = select(OAuthConnection).where(OAuthConnection.user_id == current_user.id, OAuthConnection.tenant_id == tenant_id, OAuthConnection.is_active == True)
    result = await db.execute(query)
    connections = result.scalars().all()
    return {"connections": [{"id": c.id, "provider": c.provider, "created_at": c.created_at.isoformat()} for c in connections]}

@router.post("/oauth/connect")
async def connect_oauth(data: OAuthConnect, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    connection = OAuthConnection(user_id=current_user.id, tenant_id=tenant_id, provider=data.provider, provider_user_id="temp", access_token=data.code)
    db.add(connection)
    await db.commit()
    return {"message": "Connected", "provider": data.provider}

@router.post("/webhooks")
async def create_webhook(data: WebhookCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user), tenant_id: int = Depends(get_tenant_id)):
    webhook = WebhookConfig(tenant_id=tenant_id, name=data.name, url=data.url, events=data.events, secret=data.secret)
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    return {"id": webhook.id, "name": webhook.name}

@router.get("/webhooks")
async def get_webhooks(db: AsyncSession = Depends(get_db), tenant_id: int = Depends(get_tenant_id)):
    from sqlalchemy import select
    query = select(WebhookConfig).where(WebhookConfig.tenant_id == tenant_id, WebhookConfig.is_active == True)
    result = await db.execute(query)
    webhooks = result.scalars().all()
    return {"webhooks": [{"id": w.id, "name": w.name, "url": w.url, "events": w.events} for w in webhooks]}
