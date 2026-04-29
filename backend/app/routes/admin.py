from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.middleware.rbac import require_roles
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieResponse


router = APIRouter(prefix="/admin", tags=["admin"])


# All endpoints in this router require admin role
# Using dependencies at router level to enforce this
admin_required = Depends(require_roles(["admin"]))


@router.get("/users", dependencies=[admin_required])
async def list_users():
    """List all users. Admin only. Placeholder for future implementation."""
    return {"message": "User listing - Phase 2", "users": []}


@router.post("/movies", response_model=MovieResponse, dependencies=[admin_required])
async def create_movie(movie: MovieCreate):
    """Create a new movie. Admin only. Placeholder for Phase 2."""
    return {
        "id": 1,
        "title": movie.title,
        "description": movie.description,
        "publication_status": movie.publication_status.value,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
    }


@router.get("/movies", dependencies=[admin_required])
async def list_movies_admin():
    """List all movies (including unpublished). Admin only. Placeholder for Phase 2."""
    return {"message": "Admin movie listing - Phase 2", "movies": []}


@router.get("/dashboard", dependencies=[admin_required])
async def admin_dashboard(current_user: User = Depends(get_current_user)):
    """Admin dashboard. Admin only."""
    return {
        "message": "Admin dashboard",
        "admin_email": current_user.email,
    }
