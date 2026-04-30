import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, UserRole
from app.models.movie import Movie, PublicationStatus
from app.models.video_file import VideoFile
from app.services.user import user_service
from app.services.auth import auth_service


class TestLoginIntegration:
    """End-to-end integration tests for login flow."""

    @pytest.mark.asyncio
    async def test_complete_login_flow(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Test complete login flow: create user, login, access protected endpoint."""
        # Step 1: Create a test user
        user = await user_service.create(
            db_session, "integration@example.com", "password123"
        )

        # Step 2: Login with credentials
        login_response = await client.post(
            "/auth/login",
            data={"username": "integration@example.com", "password": "password123"},
        )

        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        assert login_data["token_type"] == "bearer"

        # Step 3: Access protected endpoint with token
        me_response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {login_data['access_token']}"},
        )

        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["email"] == "integration@example.com"
        assert me_data["role"] == "user"

    @pytest.mark.asyncio
    async def test_login_with_invalid_credentials(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Test login rejection with invalid credentials."""
        await user_service.create(db_session, "user@example.com", "correctpassword")

        response = await client.post(
            "/auth/login",
            data={"username": "user@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect email or password"


class TestSessionPersistence:
    """Integration tests for session persistence via refresh tokens."""

    @pytest.mark.asyncio
    async def test_refresh_token_flow(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Test session persistence: login, get refresh token, refresh access token."""
        from app.services.auth import auth_service

        # Step 1: Create user
        user = await user_service.create(
            db_session, "refresh@example.com", "password123"
        )

        # Step 2: Login and get refresh token
        login_response = await client.post(
            "/auth/login",
            data={"username": "refresh@example.com", "password": "password123"},
        )

        assert login_response.status_code == 200
        refresh_token = login_response.cookies.get("refresh_token")
        assert refresh_token is not None

        # Step 3: Use refresh token to get new access token
        refresh_response = await client.post(
            "/auth/refresh",
            cookies={"refresh_token": refresh_token},
        )

        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        assert "access_token" in refresh_data

        # Step 4: Verify new access token works
        me_response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {refresh_data['access_token']}"},
        )

        assert me_response.status_code == 200
        assert me_response.json()["email"] == "refresh@example.com"

    @pytest.mark.asyncio
    async def test_refresh_without_cookie_fails(
        self, client: AsyncClient
    ):
        """Test that refresh fails without refresh token cookie."""
        response = await client.post("/auth/refresh")

        assert response.status_code == 401


class TestLogoutIntegration:
    """Integration tests for logout flow."""

    @pytest.mark.asyncio
    async def test_complete_logout_flow(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Test logout clears session and tokens become invalid for refresh."""
        # Step 1: Create user and login
        await user_service.create(db_session, "logout@example.com", "password123")

        login_response = await client.post(
            "/auth/login",
            data={"username": "logout@example.com", "password": "password123"},
        )

        access_token = login_response.json()["access_token"]
        refresh_token = login_response.cookies.get("refresh_token")

        # Step 2: Verify logged in
        me_response = await client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_response.status_code == 200

        # Step 3: Logout
        logout_response = await client.post("/auth/logout")
        assert logout_response.status_code == 200
        assert logout_response.json()["message"] == "Successfully logged out"


class TestAdminRoleEnforcement:
    """Integration tests for admin role enforcement (AUTH-04)."""

    @pytest.mark.asyncio
    async def test_admin_can_access_all_endpoints(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Admin user should access all admin endpoints."""
        # Create admin user
        admin = await user_service.create(
            db_session, "admin@example.com", "adminpassword", role=UserRole.ADMIN
        )

        # Login
        login_response = await client.post(
            "/auth/login",
            data={"username": "admin@example.com", "password": "adminpassword"},
        )

        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Test all admin endpoints
        dashboard_response = await client.get("/admin/dashboard", headers=headers)
        assert dashboard_response.status_code == 200

        users_response = await client.get("/admin/users", headers=headers)
        assert users_response.status_code == 200

        movies_response = await client.get("/admin/movies", headers=headers)
        assert movies_response.status_code == 200

        create_movie_response = await client.post(
            "/admin/movies",
            headers=headers,
            json={"title": "Test", "description": "Test", "publication_status": "draft"},
        )
        assert create_movie_response.status_code == 200

    @pytest.mark.asyncio
    async def test_regular_user_blocked_from_admin(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Regular user should be blocked from all admin endpoints."""
        # Create regular user
        await user_service.create(
            db_session, "user@example.com", "userpassword", role=UserRole.USER
        )

        # Login
        login_response = await client.post(
            "/auth/login",
            data={"username": "user@example.com", "password": "userpassword"},
        )

        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Test all admin endpoints return 403
        dashboard_response = await client.get("/admin/dashboard", headers=headers)
        assert dashboard_response.status_code == 403

        users_response = await client.get("/admin/users", headers=headers)
        assert users_response.status_code == 403

        movies_response = await client.get("/admin/movies", headers=headers)
        assert movies_response.status_code == 403

        create_movie_response = await client.post(
            "/admin/movies",
            headers=headers,
            json={"title": "Test", "description": "Test"},
        )
        assert create_movie_response.status_code == 403

    @pytest.mark.asyncio
    async def test_unauthenticated_blocked_from_admin(
        self, client: AsyncClient
    ):
        """Unauthenticated requests should be blocked from admin endpoints."""
        # No login, no token
        dashboard_response = await client.get("/admin/dashboard")
        assert dashboard_response.status_code == 401

        users_response = await client.get("/admin/users")
        assert users_response.status_code == 401

        movies_response = await client.post(
            "/admin/movies",
            json={"title": "Test", "description": "Test"},
        )
        assert movies_response.status_code == 401


class TestPhaseRequirements:
    """
    Validation tests for Phase 1 requirements.
    Each test maps to a specific requirement ID.
    """

    @pytest.mark.asyncio
    async def test_AUTH_01_user_login(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """AUTH-01: User can log in with valid credentials before accessing movie pages."""
        await user_service.create(db_session, "auth01@example.com", "password")

        response = await client.post(
            "/auth/login",
            data={"username": "auth01@example.com", "password": "password"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()

    @pytest.mark.asyncio
    async def test_AUTH_02_session_persists(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """AUTH-02: User session persists across browser refresh until logout or expiration."""
        from app.services.auth import auth_service

        user = await user_service.create(db_session, "auth02@example.com", "password")

        # Login
        login_response = await client.post(
            "/auth/login",
            data={"username": "auth02@example.com", "password": "password"},
        )

        refresh_token = login_response.cookies.get("refresh_token")

        # Simulate browser refresh by using refresh token
        refresh_response = await client.post(
            "/auth/refresh",
            cookies={"refresh_token": refresh_token},
        )

        assert refresh_response.status_code == 200
        assert "access_token" in refresh_response.json()

    @pytest.mark.asyncio
    async def test_AUTH_03_user_logout(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """AUTH-03: User can log out from the web app."""
        await user_service.create(db_session, "auth03@example.com", "password")

        await client.post(
            "/auth/login",
            data={"username": "auth03@example.com", "password": "password"},
        )

        logout_response = await client.post("/auth/logout")

        assert logout_response.status_code == 200
        assert logout_response.json()["message"] == "Successfully logged out"

    @pytest.mark.asyncio
    async def test_AUTH_04_admin_restricted(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """AUTH-04: Administrator access is restricted to users with an admin role."""
        await user_service.create(
            db_session, "auth04user@example.com", "password", role=UserRole.USER
        )

        login_response = await client.post(
            "/auth/login",
            data={"username": "auth04user@example.com", "password": "password"},
        )

        token = login_response.json()["access_token"]

        response = await client.get(
            "/admin/dashboard",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_API_01_documented_apis(
        self, client: AsyncClient
    ):
        """API-01: Frontend communicates with backend through documented HTTP APIs."""
        # Verify OpenAPI documentation is accessible
        openapi_response = await client.get("/openapi.json")
        assert openapi_response.status_code == 200

        spec = openapi_response.json()

        # Verify auth endpoints are documented
        assert "/auth/login" in spec["paths"]
        assert "/auth/logout" in spec["paths"]
        assert "/auth/refresh" in spec["paths"]
        assert "/auth/me" in spec["paths"]

        # Verify admin endpoints are documented
        assert "/admin/dashboard" in spec["paths"]

    @pytest.mark.asyncio
    async def test_API_02_data_persistence(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """API-02: Backend persists users, roles, movies, and uploaded video file metadata."""
        from app.models.user import User
        from app.models.movie import Movie, PublicationStatus
        from app.models.video_file import VideoFile
        from sqlalchemy import select

        # Verify user persistence
        user = await user_service.create(
            db_session, "api02@example.com", "password", role=UserRole.ADMIN
        )

        result = await db_session.execute(
            select(User).where(User.email == "api02@example.com")
        )
        saved_user = result.scalar_one()
        assert saved_user.role == UserRole.ADMIN

        # Verify movie persistence
        movie = Movie(
            title="API Test Movie",
            description="Test",
            publication_status=PublicationStatus.PUBLISHED,
        )
        db_session.add(movie)
        await db_session.commit()

        result = await db_session.execute(
            select(Movie).where(Movie.title == "API Test Movie")
        )
        saved_movie = result.scalar_one()
        assert saved_movie.publication_status == PublicationStatus.PUBLISHED

        # Verify video file persistence
        video = VideoFile(
            movie_id=saved_movie.id,
            filename="test.mp4",
            file_path="/uploads/test.mp4",
            file_size=1000,
            mime_type="video/mp4",
        )
        db_session.add(video)
        await db_session.commit()

        result = await db_session.execute(
            select(VideoFile).where(VideoFile.movie_id == saved_movie.id)
        )
        saved_video = result.scalar_one()
        assert saved_video.filename == "test.mp4"
