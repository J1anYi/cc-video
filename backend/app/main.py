from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import engine, Base
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.user import router as user_router
from app.routes.recommendations import router as recommendations_router
from app.routes.trending import router as trending_router
from app.routes.ratings import router as ratings_router
from app.routes.reviews import router as reviews_router
from app.routes.comments import router as comments_router
from app.routes.helpful_votes import router as helpful_votes_router
from app.routes.follows import router as follows_router
from app.routes.feed import router as feed_router
from app.routes.notifications import router as notifications_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev mode; use Alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="CC Video API",
    description="Backend API for CC Video streaming platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(recommendations_router)
app.include_router(trending_router)
app.include_router(ratings_router)
app.include_router(reviews_router)
app.include_router(comments_router)
app.include_router(helpful_votes_router)
app.include_router(follows_router)
app.include_router(feed_router)
app.include_router(notifications_router)

# Mount static files for posters and subtitles
posters_dir = os.path.join(settings.UPLOAD_DIR, "posters")
subtitles_dir = os.path.join(settings.UPLOAD_DIR, "subtitles")
os.makedirs(posters_dir, exist_ok=True)
os.makedirs(subtitles_dir, exist_ok=True)

app.mount("/uploads/posters", StaticFiles(directory=posters_dir), name="posters")
app.mount("/uploads/subtitles", StaticFiles(directory=subtitles_dir), name="subtitles")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
