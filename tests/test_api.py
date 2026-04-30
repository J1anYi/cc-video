import pytest
from httpx import AsyncClient


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_returns_healthy(self, client: AsyncClient):
        """Health endpoint should return status healthy."""
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestOpenAPIDocs:
    """Tests for API documentation endpoints."""

    @pytest.mark.asyncio
    async def test_openapi_json_accessible(self, client: AsyncClient):
        """OpenAPI JSON schema should be accessible."""
        response = await client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data

    @pytest.mark.asyncio
    async def test_swagger_ui_accessible(self, client: AsyncClient):
        """Swagger UI documentation should be accessible."""
        response = await client.get("/docs")

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_redoc_accessible(self, client: AsyncClient):
        """ReDoc documentation should be accessible."""
        response = await client.get("/redoc")

        assert response.status_code == 200
