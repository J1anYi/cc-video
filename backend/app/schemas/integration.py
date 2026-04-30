from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class BiometricType(str, Enum):
    FACE_ID = "face_id"
    TOUCH_ID = "touch_id"
    FINGERPRINT = "fingerprint"
    NONE = "none"

class PaymentProvider(str, Enum):
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    CARRIER_BILLING = "carrier_billing"

class DeepLink(BaseModel):
    url: str
    path: str
    params: Dict[str, str]

class BiometricAuthRequest(BaseModel):
    biometric_type: BiometricType
    device_id: str
    challenge: str

class BiometricAuthResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    expires_at: Optional[datetime] = None

class PaymentRequest(BaseModel):
    provider: PaymentProvider
    amount: float
    currency: str = "USD"
    product_id: str
    user_id: int

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    provider: PaymentProvider
    created_at: datetime

class CastDevice(BaseModel):
    id: str
    name: str
    type: str
    is_available: bool

class WidgetConfig(BaseModel):
    widget_type: str
    movie_ids: List[int]
    refresh_interval: int = 3600
