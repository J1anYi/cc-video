"""Phase 203: Global Payment Routes"""
from fastapi import APIRouter, Body
from typing import List
from ..services.global_payment import GlobalPaymentService

router = APIRouter(prefix="/api/global-payment", tags=["global-payment"])
service = GlobalPaymentService()

@router.post("/currency/{tenant_id}")
async def manage_currency(tenant_id: str, currencies: List[str] = Body(default=[])):
    return await service.manage_multi_currency(tenant_id, currencies)

@router.post("/regional/{region}")
async def setup_regional(region: str, payment_methods: List[str] = Body(default=[])):
    return await service.setup_regional_payments(region, payment_methods)

@router.post("/pricing/{content_id}")
async def config_pricing(content_id: str, pricing_config: dict):
    return await service.configure_dynamic_pricing(content_id, pricing_config)

@router.post("/tax/{region}")
async def setup_tax(region: str):
    return await service.setup_tax_compliance(region)

@router.post("/fraud/{tenant_id}")
async def config_fraud(tenant_id: str):
    return await service.configure_fraud_prevention(tenant_id)
