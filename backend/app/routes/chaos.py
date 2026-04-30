from fastapi import APIRouter
router = APIRouter(prefix="/chaos", tags=["chaos"])
@router.get("/experiments")
async def list_experiments(): return {"experiments": []}
@router.post("/experiments")
async def create_experiment(name: str, failure_type: str): return {"id": "1", "name": name, "type": failure_type}
@router.post("/experiments/{exp_id}/run")
async def run_experiment(exp_id: str): return {"status": "running", "exp_id": exp_id}
@router.get("/resilience-score")
async def get_resilience_score(): return {"score": 95.5, "tests_passed": 10, "tests_failed": 1}
