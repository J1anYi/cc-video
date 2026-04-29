import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserRole
from app.services.user import user_service
from app.services.auth import auth_service


class TestAdminEndpoints:
    """Tests for admin endpoint access control."""

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
    async def test_admin_can_access_dashboard(
        self, client: AsyncClient, admin_token: str
    ):
        """Admin user should be able to access admin dashboard."""
        response = await client.get(
            "/admin/dashboard",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "admin_email" in data
        assert data["admin_email"] == "admin@example.com"

    @pytest.mark.asyncio
    async def test_admin_can_list_users(
        self, client: AsyncClient, admin_token: str
    ):
        """Admin user should be able to list users."""
        response = await client.get(
            "/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_admin_can_create_movies(
        self, client: AsyncClient, admin_token: str
    ):
        """Admin user should be able to create movies."""
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

    @pytest.mark.asyncio
    async def test_regular_user_cannot_access_dashboard(
        self, client: AsyncClient, user_token: str
    ):
        """Regular user should be forbidden from admin dashboard."""
        response = await client.get(
            "/admin/dashboard",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403
        assert response.json()["detail"] == "Not enough permissions"

    @pytest.mark.asyncio
    async def test_regular_user_cannot_list_users(
        self, client: AsyncClient, user_token: str
    ):
        """Regular user should be forbidden from listing users."""
        response = await client.get(
            "/admin/users",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_regular_user_cannot_create_movies(
        self, client: AsyncClient, user_token: str
    ):
        """Regular user should be forbidden from creating movies."""
        response = await client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "title": "Test Movie",
                "description": "A test movie",
            },
        )

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_unauthenticated_user_cannot_access_admin(
        self, client: AsyncClient
    ):
        """Unauthenticated user should be forbidden from admin endpoints."""
        response = await client.get("/admin/dashboard")

        # Should be 401 (Unauthorized) due to missing auth, not 403
        assert response.status_code == 401


class TestRoleChecking:
    """Tests for role checking logic."""

    @pytest.mark.asyncio
    async def test_admin_role_value(self, db_session: AsyncSession):
        """Admin user should have role value 'admin'."""
        admin = await user_service.create(
            db_session, "admin@example.com", "password", role=UserRole.ADMIN
        )

        assert admin.role == UserRole.ADMIN
        assert admin.role.value == "admin"

    @pytest.mark.asyncio
    async def test_user_role_value(self, db_session: AsyncSession):
        """Regular user should have role value 'user'."""
        user = await user_service.create(
            db_session, "user@example.com", "password", role=UserRole.USER
        )

        assert user.role == UserRole.USER
        assert user.role.value == "user"
