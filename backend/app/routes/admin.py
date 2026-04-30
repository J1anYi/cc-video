from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
import math

from app.dependencies import get_current_user, get_db
from app.middleware.rbac import require_roles
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse, MovieListResponse
from app.schemas.video_file import VideoFileResponse
from app.schemas.subtitle import SubtitleResponse, SubtitleListResponse
from app.schemas.user import UserAdminView, UserListResponse, UserSuspensionRequest
from app.services.movie import movie_service
from app.services.video_file import video_file_service
from app.services.poster import poster_service
from app.services.subtitle import subtitle_service
from app.services.admin_user import admin_user_service


router = APIRouter(prefix="/admin", tags=["admin"])


# All endpoints in this router require admin role
admin_required = Depends(require_roles(["admin"]))


@router.get("/users", response_model=UserListResponse, dependencies=[admin_required])
async def list_users(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
):
    """List all users with pagination. Admin only."""
    users, total = await admin_user_service.list_users(db, page, limit, search)
    total_pages = math.ceil(total / limit) if limit > 0 else 0
    return UserListResponse(
        users=[UserAdminView.model_validate(u) for u in users],
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
    )


@router.get("/users/{user_id}", response_model=UserAdminView, dependencies=[admin_required])
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get user details. Admin only."""
    user = await admin_user_service.get_user_details(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserAdminView.model_validate(user)


@router.patch("/users/{user_id}/suspend", response_model=UserAdminView, dependencies=[admin_required])
async def toggle_user_suspension(
    user_id: int,
    request: UserSuspensionRequest,
    db: AsyncSession = Depends(get_db),
):
    """Suspend or unsuspend a user. Admin only."""
    user = await admin_user_service.suspend_user(db, user_id, request.suspend)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserAdminView.model_validate(user)


@router.delete("/users/{user_id}", status_code=204, dependencies=[admin_required])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Soft delete a user. Admin only."""
    user = await admin_user_service.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return None


@router.post("/movies", response_model=MovieResponse, dependencies=[admin_required])
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db)):
    """Create a new movie. Admin only."""
    return await movie_service.create(db, movie)


@router.get("/movies", response_model=MovieListResponse, dependencies=[admin_required])
async def list_movies_admin(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    """List all movies (including unpublished). Admin only."""
    movies = await movie_service.get_all(db, skip, limit)
    return MovieListResponse(movies=movies, total=len(movies))


@router.get("/movies/{movie_id}", response_model=MovieResponse, dependencies=[admin_required])
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single movie by ID. Admin only."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.patch("/movies/{movie_id}", response_model=MovieResponse, dependencies=[admin_required])
async def update_movie(movie_id: int, movie_update: MovieUpdate, db: AsyncSession = Depends(get_db)):
    """Update a movie. Admin only."""
    movie = await movie_service.update(db, movie_id, movie_update)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.delete("/movies/{movie_id}", status_code=204, dependencies=[admin_required])
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a movie. Admin only."""
    deleted = await movie_service.delete(db, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None


@router.post("/movies/{movie_id}/video", response_model=VideoFileResponse, dependencies=[admin_required])
async def upload_video(movie_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Upload a video file for a movie. Admin only."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    try:
        video_file = await video_file_service.upload(db, movie_id, file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return video_file


@router.delete("/movies/{movie_id}/video", status_code=204, dependencies=[admin_required])
async def delete_video(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Delete video file from a movie. Admin only."""
    video_files = await video_file_service.get_by_movie(db, movie_id)
    if not video_files:
        raise HTTPException(status_code=404, detail="No video file found")
    await video_file_service.delete(db, video_files[0].id)
    return None


@router.post("/movies/{movie_id}/poster", response_model=MovieResponse, dependencies=[admin_required])
async def upload_poster(movie_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Upload a poster image for a movie. Admin only."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    try:
        poster_path = await poster_service.upload(db, movie_id, file)
        movie = await movie_service.update(db, movie_id, MovieUpdate())
        # Directly update poster_path
        movie.poster_path = poster_path
        await db.commit()
        await db.refresh(movie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return movie


@router.delete("/movies/{movie_id}/poster", status_code=204, dependencies=[admin_required])
async def delete_poster(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Delete poster image from a movie. Admin only."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    poster_service.delete(movie.poster_path)
    movie.poster_path = None
    await db.commit()
    return None


@router.post("/movies/{movie_id}/subtitles", response_model=SubtitleResponse, dependencies=[admin_required])
async def upload_subtitle(
    movie_id: int,
    language: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a subtitle file for a movie. Admin only."""
    movie = await movie_service.get_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    try:
        subtitle = await subtitle_service.upload(db, movie_id, language, file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return subtitle


@router.get("/movies/{movie_id}/subtitles", response_model=SubtitleListResponse, dependencies=[admin_required])
async def list_subtitles(movie_id: int, db: AsyncSession = Depends(get_db)):
    """List all subtitles for a movie. Admin only."""
    subtitles = await subtitle_service.get_by_movie(db, movie_id)
    return SubtitleListResponse(subtitles=subtitles)


@router.delete("/movies/{movie_id}/subtitles/{subtitle_id}", status_code=204, dependencies=[admin_required])
async def delete_subtitle(movie_id: int, subtitle_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a subtitle file from a movie. Admin only."""
    deleted = await subtitle_service.delete(db, subtitle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subtitle not found")
    return None


@router.get("/dashboard", dependencies=[admin_required])
async def admin_dashboard(current_user: User = Depends(get_current_user)):
    """Admin dashboard. Admin only."""
    return {
        "message": "Admin dashboard",
        "admin_email": current_user.email,
    }
