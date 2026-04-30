from fastapi import APIRouter
router = APIRouter(prefix="/feature-flags", tags=["feature-flags"])
flags = {"dark_mode": True, "new_ui": False}
@router.get("/")
async def list_flags(): return {"flags": flags}
@router.post("/{name}")
async def set_flag(name: str, enabled: bool): flags[name] = enabled; return {"name": name, "enabled": enabled}
@router.get("/{name}")
async def get_flag(name: str): return {"name": name, "enabled": flags.get(name, False)}
