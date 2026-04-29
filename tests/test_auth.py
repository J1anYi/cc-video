import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.services.user import user_service
from app.services.auth import auth_service


class TestLoginEndpoint:
    """Tests for POST /auth/login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, db_session: AsyncSession):
        """Login with valid credentials should return access token."""
        await user_service.create(db_session, "test@example.com", "password123")

        response = await client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_sets_refresh_cookie(self, client: AsyncClient, db_session: AsyncSession):
        """Login should set refresh_token cookie."""
        await user_service.create(db_session, "test@example.com", "password123")

        response = await client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "password123"},
        )

        assert response.status_code == 200
        cookies = response.cookies
        assert "refresh_token" in cookies

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client: AsyncClient, db_session: AsyncSession):
        """Login with wrong password should return 401."""
        await user_service.create(db_session, "test@example.com", "password123")

        response = await client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, client: AsyncClient, db_session: AsyncSession):
        """Login with non-existent email should return 401."""
        response = await client.post(
            "/auth/login",
            data={"username": "nonexistent@example.com", "password": "password123"},
        )

        assert response.status_code == 401


class TestLogoutEndpoint:
    """Tests for POST /auth/logout endpoint."""

    @pytest.mark.asyncio
    async def test_logout_clears_cookie(self, client: AsyncClient):
        """Logout should clear refresh_token cookie."""
        response = await client.post("/auth/logout")

        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"


class TestRefreshEndpoint:
    """Tests for POST /auth/refresh endpoint."""

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client: AsyncClient, db_session: AsyncSession):
        """Refresh with valid token should return new access token."""
        user = await user_service.create(db_session, "test@example.com", "password123")
        refresh_token = auth_service.create_refresh_token(str(user.id))

        response = await client.post(
            "/auth/refresh",
            cookies={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_refresh_without_cookie(self, client: AsyncClient):
        """Refresh without cookie should return 401."""
        response = await client.post("/auth/refresh")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_with_invalid_token(self, client: AsyncClient):
        """Refresh with invalid token should return 401."""
        response = await client.post(
            "/auth/refresh",
            cookies={"refresh_token": "invalid_token"},
        )

        assert response.status_code == 401


class TestMeEndpoint:
    """Tests for GET /auth/me endpoint."""

    @pytest.mark.asyncio
    async def test_me_with_valid_token(self, client: AsyncClient, db_session: AsyncSession):
        """Me endpoint should return current user profile."""
        user = await user_service.create(db_session, "test@example.com", "password123")
        access_token = auth_service.create_access_token(str(user.id), user.role.value)

        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "user"

    @pytest.mark.asyncio
    async def test_me_without_token(self, client: AsyncClient):
        """Me endpoint without token should return 401."""
        response = await client.get("/auth/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_with_invalid_token(self, client: AsyncClient):
        """Me endpoint with invalid token should return 401."""
        response = await client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_admin_user(self, client: AsyncClient, db_session: AsyncSession):
        """Me endpoint should return admin role for admin user."""
        user = await user_service.create(
            db_session, "admin@example.com", "password123", role=UserRole.ADMIN
        )
        access_token = auth_service.create_access_token(str(user.id), user.role.value)

        response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
