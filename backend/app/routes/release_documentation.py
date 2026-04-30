from fastapi import APIRouter
from typing import Dict, Any
from app.services.release_documentation import release_documentation_service

router = APIRouter(prefix="/api/release-docs", tags=["release-documentation"])

@router.post("/release-notes")
async def release_notes() -> Dict[str, Any]:
    return await release_documentation_service.create_release_notes()

@router.post("/migration-guide")
async def migration_guide() -> Dict[str, Any]:
    return await release_documentation_service.create_migration_guide()

@router.post("/runbooks")
async def runbooks() -> Dict[str, Any]:
    return await release_documentation_service.create_runbooks()

@router.post("/api-docs")
async def api_docs() -> Dict[str, Any]:
    return await release_documentation_service.update_api_docs()

@router.post("/deployment-guides")
async def deployment_guides() -> Dict[str, Any]:
    return await release_documentation_service.create_deployment_guides()
