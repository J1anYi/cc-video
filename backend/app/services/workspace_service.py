from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class WorkspaceService:
    async def create_workspace(self, db: AsyncSession, name: str, owner_id: int) -> dict:
        return {'id': 1, 'name': name, 'owner_id': owner_id}
    async def add_member(self, db: AsyncSession, workspace_id: int, user_id: int, role: str) -> dict:
        return {'workspace_id': workspace_id, 'user_id': user_id, 'role': role}
    async def list_workspaces(self, db: AsyncSession, user_id: int) -> list:
        return []

workspace_service = WorkspaceService()
