import io
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRole
from app.services.user import user_service
from app.services.auth import auth_service


class TestAdminMovieRoutes:
    """Integration tests for admin movie routes."""

    @pytest.fixture
    async def admin_user(self, db_session: AsyncSession):
        """Create an admin user for testing."""
        return await user_service.create(
            db_session, "admin@example.com", "adminpassword", role=UserRole.ADMIN
        )

    @pytest.fixture
    async def regular_user(self, db_session: AsyncSession):
        """Create a regular user for testing."""
        return await user_service.create(
            db_session, "user@example.com", "userpassword", role=UserRole.USER
        )

    @pytest.fixture
    def admin_token(self, admin_user):
        """Get access token for admin user."""
        return auth_service.create_access_token(str(admin_user.id), admin_user.role.value)

    @pytest.fixture
    def user_token(self, regular_user):
        """Get access token for regular user."""
        return auth_service.create_access_token(str(regular_user.id), regular_user.role.value)

    @pytest.mark.asyncio
    async def test_create_movie(self, client: AsyncClient, admin_token: str):
        """Admin can create a movie."""
        response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "title": "Test Movie",
                "description": "A test movie",
                "publication_status": "draft",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Movie"
        assert data["description"] == "A test movie"
        assert data["publication_status"] == "draft"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_movie_with_status(self, client: AsyncClient, admin_token: str):
        """Admin can create a movie with PUBLISHED status."""
        response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "title": "Published Movie",
                "description": "Already published",
                "publication_status": "published",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["publication_status"] == "published"

    @pytest.mark.asyncio
    async def test_list_movies(self, client: AsyncClient, admin_token: str):
        """Admin can list all movies including unpublished."""
        await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie 1", "publication_status": "draft"},
        )
        await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie 2", "publication_status": "published"},
        )

        response = await client.get(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["movies"]) == 2
        assert data["total"] == 2

    @pytest.mark.asyncio
    async def test_get_movie(self, client: AsyncClient, admin_token: str):
        """Admin can get a single movie by ID."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Test Movie", "description": "Description"},
        )
        movie_id = create_response.json()["id"]

        response = await client.get(
            f"/admin/movies/{movie_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == movie_id
        assert data["title"] == "Test Movie"

    @pytest.mark.asyncio
    async def test_get_movie_not_found(self, client: AsyncClient, admin_token: str):
        """Admin gets 404 for non-existent movie."""
        response = await client.get(
            "/admin/movies/999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Movie not found"

    @pytest.mark.asyncio
    async def test_update_movie_title(self, client: AsyncClient, admin_token: str):
        """Admin can update movie title."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Original Title"},
        )
        movie_id = create_response.json()["id"]

        response = await client.patch(
            f"/admin/movies/{movie_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Updated Title"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    @pytest.mark.asyncio
    async def test_update_movie_status(self, client: AsyncClient, admin_token: str):
        """Admin can update publication status."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie", "publication_status": "draft"},
        )
        movie_id = create_response.json()["id"]

        response = await client.patch(
            f"/admin/movies/{movie_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"publication_status": "published"},
        )
        assert response.status_code == 200
        assert response.json()["publication_status"] == "published"

    @pytest.mark.asyncio
    async def test_update_movie_partial(self, client: AsyncClient, admin_token: str):
        """Admin can perform partial update."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie", "description": "Original desc"},
        )
        movie_id = create_response.json()["id"]

        response = await client.patch(
            f"/admin/movies/{movie_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"description": "New description"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "New description"
        assert data["title"] == "Movie"

    @pytest.mark.asyncio
    async def test_delete_movie(self, client: AsyncClient, admin_token: str):
        """Admin can delete a movie."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "To Delete"},
        )
        movie_id = create_response.json()["id"]

        response = await client.delete(
            f"/admin/movies/{movie_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

        get_response = await client.get(
            f"/admin/movies/{movie_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_movie_not_found(self, client: AsyncClient, admin_token: str):
        """Admin gets 404 when deleting non-existent movie."""
        response = await client.delete(
            "/admin/movies/999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_upload_video(self, client: AsyncClient, admin_token: str):
        """Admin can upload a video file to a movie."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie with Video"},
        )
        movie_id = create_response.json()["id"]

        video_content = b"fake video content for testing"
        video_file = io.BytesIO(video_content)

        response = await client.post(
            f"/admin/movies/{movie_id}/video",
            headers={"Authorization": f"Bearer {admin_token}"},
            files={"file": ("test.mp4", video_file, "video/mp4")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["movie_id"] == movie_id
        assert data["filename"] == "test.mp4"
        assert data["mime_type"] == "video/mp4"
        assert data["file_size"] == len(video_content)

    @pytest.mark.asyncio
    async def test_upload_video_invalid_type(self, client: AsyncClient, admin_token: str):
        """Upload is rejected for non-video MIME type."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie"},
        )
        movie_id = create_response.json()["id"]

        text_file = io.BytesIO(b"not a video")

        response = await client.post(
            f"/admin/movies/{movie_id}/video",
            headers={"Authorization": f"Bearer {admin_token}"},
            files={"file": ("test.txt", text_file, "text/plain")},
        )
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_upload_video_movie_not_found(self, client: AsyncClient, admin_token: str):
        """Upload is rejected if movie doesn't exist."""
        video_file = io.BytesIO(b"fake video")

        response = await client.post(
            "/admin/movies/999/video",
            headers={"Authorization": f"Bearer {admin_token}"},
            files={"file": ("test.mp4", video_file, "video/mp4")},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_video(self, client: AsyncClient, admin_token: str):
        """Admin can remove video from movie."""
        create_response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"title": "Movie"},
        )
        movie_id = create_response.json()["id"]

        video_file = io.BytesIO(b"fake video")
        await client.post(
            f"/admin/movies/{movie_id}/video",
            headers={"Authorization": f"Bearer {admin_token}"},
            files={"file": ("test.mp4", video_file, "video/mp4")},
        )

        response = await client.delete(
            f"/admin/movies/{movie_id}/video",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_regular_user_cannot_create_movie(
        self, client: AsyncClient, user_token: str
    ):
        """Regular user cannot create movies."""
        response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"title": "Test"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_unauthenticated_user_cannot_access_admin(
        self, client: AsyncClient
    ):
        """Unauthenticated user cannot access admin endpoints."""
        response = await client.get("/admin/movies")
        assert response.status_code == 403  # Forbidden (no token provided)
