from fastapi import APIRouter
router = APIRouter(prefix="/capacity", tags=["capacity"])
@router.get("/forecast")
async def get_forecast(): return {"cpu": {"current": 45, "predicted_7d": 52}, "memory": {"current": 60, "predicted_7d": 68}}
@router.get("/costs")
async def get_costs(): return {"monthly": 5000, "by_service": {"api": 2000, "db": 1500, "cdn": 1500}}
@router.get("/scaling")
async def get_scaling_status(): return {"current_instances": 3, "min": 2, "max": 10, "target_cpu": 70}
