import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.models.movie import Movie, PublicationStatus
from app.models.video_file import VideoFile


class TestUserModel:
    """Tests for User model persistence."""

    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        """User should be persistable to database."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_here",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()

        result = await db_session.execute(select(User).where(User.email == "test@example.com"))
        saved_user = result.scalar_one()

        assert saved_user.id is not None
        assert saved_user.email == "test@example.com"
        assert saved_user.role == UserRole.USER
        assert saved_user.is_active is True

    @pytest.mark.asyncio
    async def test_create_admin_user(self, db_session: AsyncSession):
        """Admin user should have ADMIN role."""
        user = User(
            email="admin@example.com",
            hashed_password="hashed_password_here",
            role=UserRole.ADMIN,
        )
        db_session.add(user)
        await db_session.commit()

        result = await db_session.execute(select(User).where(User.email == "admin@example.com"))
        saved_user = result.scalar_one()

        assert saved_user.role == UserRole.ADMIN


class TestMovieModel:
    """Tests for Movie model persistence."""

    @pytest.mark.asyncio
    async def test_create_movie(self, db_session: AsyncSession):
        """Movie should be persistable to database."""
        movie = Movie(
            title="Test Movie",
            description="A test movie description",
            publication_status=PublicationStatus.DRAFT,
        )
        db_session.add(movie)
        await db_session.commit()

        result = await db_session.execute(select(Movie).where(Movie.title == "Test Movie"))
        saved_movie = result.scalar_one()

        assert saved_movie.id is not None
        assert saved_movie.title == "Test Movie"
        assert saved_movie.publication_status == PublicationStatus.DRAFT

    @pytest.mark.asyncio
    async def test_movie_published_status(self, db_session: AsyncSession):
        """Movie can be published."""
        movie = Movie(
            title="Published Movie",
            publication_status=PublicationStatus.PUBLISHED,
        )
        db_session.add(movie)
        await db_session.commit()

        result = await db_session.execute(select(Movie).where(Movie.title == "Published Movie"))
        saved_movie = result.scalar_one()

        assert saved_movie.publication_status == PublicationStatus.PUBLISHED


class TestVideoFileModel:
    """Tests for VideoFile model persistence."""

    @pytest.mark.asyncio
    async def test_create_video_file(self, db_session: AsyncSession):
        """VideoFile should be persistable and linked to movie."""
        # Create movie first
        movie = Movie(title="Movie with Video")
        db_session.add(movie)
        await db_session.commit()

        # Create video file
        video_file = VideoFile(
            movie_id=movie.id,
            filename="test_video.mp4",
            file_path="/uploads/test_video.mp4",
            file_size=1024000,
            mime_type="video/mp4",
        )
        db_session.add(video_file)
        await db_session.commit()

        result = await db_session.execute(
            select(VideoFile).where(VideoFile.filename == "test_video.mp4")
        )
        saved_file = result.scalar_one()

        assert saved_file.id is not None
        assert saved_file.movie_id == movie.id
        assert saved_file.filename == "test_video.mp4"
        assert saved_file.mime_type == "video/mp4"

    @pytest.mark.asyncio
    async def test_video_file_relationship(self, db_session: AsyncSession):
        """VideoFile should have relationship to Movie."""
        movie = Movie(title="Movie for Relationship Test")
        db_session.add(movie)
        await db_session.commit()

        video_file = VideoFile(
            movie_id=movie.id,
            filename="related_video.mp4",
            file_path="/uploads/related_video.mp4",
            file_size=2048000,
            mime_type="video/mp4",
        )
        db_session.add(video_file)
        await db_session.commit()
        await db_session.refresh(video_file)

        assert video_file.movie is not None
        assert video_file.movie.title == "Movie for Relationship Test"
