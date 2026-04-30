from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.integration import (
    DeepLink, BiometricType, BiometricAuthRequest, BiometricAuthResponse,
    PaymentProvider, PaymentRequest, PaymentResponse, CastDevice, WidgetConfig
)
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/mobile/integration", tags=["mobile-integration"])

def get_current_user_id(x_user_id: str = Header(...)) -> int:
    return int(x_user_id)

@router.post("/deep-link")
def handle_deep_link(url: str):
    return DeepLink(url=url, path="/movies/1", params={"id": "1"})

@router.post("/biometric/auth", response_model=BiometricAuthResponse)
def biometric_auth(request: BiometricAuthRequest, user_id: int = Depends(get_current_user_id)):
    return BiometricAuthResponse(success=True, token=str(uuid.uuid4()), expires_at=datetime.utcnow() + timedelta(hours=24))

@router.post("/payment", response_model=PaymentResponse)
def process_payment(request: PaymentRequest, db: Session = Depends(get_db)):
    return PaymentResponse(transaction_id=str(uuid.uuid4()), status="completed", provider=request.provider, created_at=datetime.utcnow())

@router.get("/cast/devices", response_model=List[CastDevice])
def get_cast_devices():
    return []

@router.get("/widget/config", response_model=WidgetConfig)
def get_widget_config(user_id: int = Depends(get_current_user_id)):
    return WidgetConfig(widget_type="continue_watching", movie_ids=[])
