from fastapi import APIRouter
from typing import Dict, Any
from app.services.technical_debt import technical_debt_service

router = APIRouter(prefix="/api/tech-debt", tags=["technical-debt"])

@router.post("/cleanup")
async def cleanup() -> Dict[str, Any]:
    return await technical_debt_service.cleanup_code()

@router.post("/dependencies")
async def update_deps() -> Dict[str, Any]:
    return await technical_debt_service.update_dependencies()

@router.post("/tests")
async def improve_tests() -> Dict[str, Any]:
    return await technical_debt_service.improve_test_coverage()

@router.post("/docs")
async def update_docs() -> Dict[str, Any]:
    return await technical_debt_service.update_docs()

@router.post("/security")
async def security_remediation() -> Dict[str, Any]:
    return await technical_debt_service.security_remediation()
