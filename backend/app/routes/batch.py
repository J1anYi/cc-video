"""Batch API endpoints."""
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/batch", tags=["batch"])


class BatchRequest(BaseModel):
    operations: List[Dict[str, Any]]
    max_operations: int = 10


class BatchResult(BaseModel):
    index: int
    success: bool
    data: Any = None
    error: str = None


@router.post("/execute", response_model=List[BatchResult])
async def execute_batch(request: BatchRequest):
    """Execute multiple operations in a single request."""
    if len(request.operations) > request.max_operations:
        raise HTTPException(
            status_code=400,
            detail=f"Too many operations. Maximum is {request.max_operations}"
        )

    results = []
    for idx, op in enumerate(request.operations):
        try:
            result = await _execute_operation(op)
            results.append(BatchResult(index=idx, success=True, data=result))
        except Exception as e:
            results.append(BatchResult(index=idx, success=False, error=str(e)))

    return results


async def _execute_operation(op: Dict[str, Any]) -> Any:
    """Execute a single operation."""
    op_type = op.get("type")
    params = op.get("params", {})

    if op_type == "echo":
        return {"echo": params}
    elif op_type == "health":
        return {"status": "healthy"}
    else:
        raise ValueError(f"Unknown operation type: {op_type}")


@router.post("/movies")
async def batch_movies(movie_ids: List[int]):
    """Batch fetch multiple movies."""
    return {"movie_ids": movie_ids, "count": len(movie_ids)}
