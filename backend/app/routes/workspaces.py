from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.post("/")
async def create_workspace(name: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return {"id": 1, "name": name}

@router.get("/")
async def list_workspaces(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return []

@router.post("/{id}/members")
async def add_member(id: int, user_id: int, role: str, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return {"status": "added"}
