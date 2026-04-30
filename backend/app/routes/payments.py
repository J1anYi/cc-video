import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import os

from app.dependencies import get_current_user
from app.models.user import User

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
router = APIRouter(prefix="/payments", tags=["payments"])

class CreatePaymentIntent(BaseModel):
    amount: int
    currency: str = "usd"
    subscription_tier: str

class PaymentMethodAttach(BaseModel):
    payment_method_id: str

@router.post("/create-intent")
async def create_payment_intent(data: CreatePaymentIntent, current_user: User = Depends(get_current_user)):
    intent = stripe.PaymentIntent.create(
        amount=data.amount,
        currency=data.currency,
        metadata={"user_id": current_user.id, "tier": data.subscription_tier}
    )
    return {"client_secret": intent.client_secret}

@router.post("/attach-method")
async def attach_payment_method(data: PaymentMethodAttach, current_user: User = Depends(get_current_user)):
    if not current_user.stripe_customer_id:
        customer = stripe.Customer.create(email=current_user.email)
        current_user.stripe_customer_id = customer.id
    stripe.PaymentMethod.attach(data.payment_method_id, customer=current_user.stripe_customer_id)
    return {"message": "Payment method attached"}

@router.get("/methods")
async def get_payment_methods(current_user: User = Depends(get_current_user)):
    if not current_user.stripe_customer_id:
        return {"methods": []}
    methods = stripe.PaymentMethod.list(customer=current_user.stripe_customer_id, type="card")
    return {"methods": methods.data}

@router.post("/refund")
async def create_refund(payment_intent_id: str, current_user: User = Depends(get_current_user)):
    refund = stripe.Refund.create(payment_intent=payment_intent_id)
    return {"refund_id": refund.id, "status": refund.status}
