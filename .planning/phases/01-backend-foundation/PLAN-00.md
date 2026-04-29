---
wave: 0
depends_on: []
files_modified:
  - backend/requirements.txt
  - backend/pyproject.toml
  - backend/app/__init__.py
  - backend/app/main.py
  - backend/app/config.py
  - backend/app/database.py
  - backend/app/dependencies.py
  - backend/data/.gitkeep
  - backend/.env.example
  - tests/__init__.py
  - tests/conftest.py
  - pytest.ini
requirements_addressed:
  - API-01
  - API-02
autonomous: true
---

# Wave 0: Test Infrastructure Setup

<objective>
Set up the FastAPI project structure with async SQLite support, pytest configuration, and shared test fixtures. Establish the foundational configuration patterns that subsequent waves will build upon.
</objective>

<must_haves>
- FastAPI application instance running with uvicorn
- Async SQLAlchemy engine configured with aiosqlite driver
- Pydantic Settings for environment configuration
- pytest configured for async tests with test database isolation
- Shared fixtures for test client, async database session, and test users
</must_haves>

<tasks>
<task id="0.1">
<name>Create backend directory structure and install dependencies</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Standard Stack section for package versions)
</read_first>
<action>
Create the backend directory with the following structure and files:

1. Create `backend/requirements.txt` with:
```
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
sqlalchemy>=2.0.0
aiosqlite>=0.21.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
alembic>=1.13.0
python-multipart>=0.0.6
```

2. Create `backend/pyproject.toml` with:
```toml
[project]
name = "cc-video-backend"
version = "0.1.0"
requires-python = ">=3.10"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["../tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

3. Create `backend/data/.gitkeep` (empty file to track directory)

4. Create `backend/.env.example` with:
```
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
DATABASE_URL=sqlite+aiosqlite:///./data/cc_video.db
DEBUG=false
CORS_ORIGINS=["http://localhost:5173"]
```

5. Create empty `backend/app/__init__.py`
</action>
<acceptance_criteria>
- File `backend/requirements.txt` exists and contains "fastapi", "sqlalchemy>=2.0.0", "aiosqlite"
- File `backend/pyproject.toml` exists and contains "asyncio_mode = \"auto\""
- File `backend/data/.gitkeep` exists
- File `backend/.env.example` exists and contains "SECRET_KEY="
</acceptance_criteria>
</task>

<task id="0.2">
<name>Create Pydantic Settings configuration</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Configuration with Pydantic Settings pattern)
  - backend/requirements.txt (created in task 0.1)
</read_first>
<action>
Create `backend/app/config.py` with exactly:

```python
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CC Video"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/cc_video.db"
    
    # Authentication
    SECRET_KEY: str  # Required, no default - must be set via env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
```
</action>
<acceptance_criteria>
- File `backend/app/config.py` exists
- File contains `class Settings(BaseSettings):`
- File contains `DATABASE_URL: str = "sqlite+aiosqlite:///./data/cc_video.db"`
- File contains `SECRET_KEY: str` (no default)
- File contains `CORS_ORIGINS: List[str]`
</acceptance_criteria>
</task>

<task id="0.3">
<name>Create async database engine and session factory</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pattern 1: Async Database Session)
  - backend/app/config.py (created in task 0.2)
</read_first>
<action>
Create `backend/app/database.py` with exactly:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass
```
</action>
<acceptance_criteria>
- File `backend/app/database.py` exists
- File contains `from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker`
- File contains `engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)`
- File contains `class Base(DeclarativeBase):`
- File contains `AsyncSessionLocal = async_sessionmaker(`
</acceptance_criteria>
</task>

<task id="0.4">
<name>Create database dependency and placeholder current_user dependency</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pattern 1 and Pattern 3)
  - backend/app/database.py (created in task 0.3)
</read_first>
<action>
Create `backend/app/dependencies.py` with exactly:

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Placeholder - will be implemented in Wave 2
async def get_current_user():
    """Dependency to get current user from JWT token. Implemented in Wave 2."""
    pass
```
</action>
<acceptance_criteria>
- File `backend/app/dependencies.py` exists
- File contains `async def get_db() -> AsyncGenerator[AsyncSession, None]:`
- File contains `async with AsyncSessionLocal() as session:`
- File contains `async def get_current_user():`
</acceptance_criteria>
</task>

<task id="0.5">
<name>Create FastAPI main application with CORS and health endpoint</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (FastAPI Main Application pattern)
  - backend/app/config.py (created in task 0.2)
  - backend/app/database.py (created in task 0.3)
</read_first>
<action>
Create `backend/app/main.py` with exactly:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base


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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```
</action>
<acceptance_criteria>
- File `backend/app/main.py` exists
- File contains `app = FastAPI(title="CC Video API"`
- File contains `CORSMiddleware`
- File contains `allow_credentials=True`
- File contains `@app.get("/health")`
- File contains `return {"status": "healthy"}`
</acceptance_criteria>
</task>

<task id="0.6">
<name>Create pytest configuration</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Test Framework section)
</read_first>
<action>
Create `pytest.ini` in project root with:

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
filterwarnings =
    ignore::DeprecationWarning
```

Create `tests/__init__.py` (empty file).
</action>
<acceptance_criteria>
- File `pytest.ini` exists at project root
- File contains `asyncio_mode = auto`
- File contains `testpaths = tests`
- File `tests/__init__.py` exists
</acceptance_criteria>
</task>

<task id="0.7">
<name>Create test fixtures with async database and test client</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Test Framework section, Wave 0 Gaps)
  - backend/app/main.py (created in task 0.5)
  - backend/app/database.py (created in task 0.3)
  - backend/app/config.py (created in task 0.2)
</read_first>
<action>
Create `tests/conftest.py` with exactly:

```python
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings


# Test database URL (in-memory SQLite for speed)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database session override."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user_data() -> dict:
    """Provide test user data for registration/login tests."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
    }


@pytest_asyncio.fixture
async def admin_user_data() -> dict:
    """Provide admin user data for admin tests."""
    return {
        "email": "admin@example.com",
        "password": "adminpassword123",
    }
```
</action>
<acceptance_criteria>
- File `tests/conftest.py` exists
- File contains `TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"`
- File contains `async def db_session() -> AsyncGenerator[AsyncSession, None]:`
- File contains `async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:`
- File contains `async def test_user_data() -> dict:`
- File contains `async def admin_user_data() -> dict:`
- File contains `app.dependency_overrides[get_db] = override_get_db`
</acceptance_criteria>
</task>

<task id="0.8">
<name>Create initial smoke tests for health and OpenAPI docs</name>
<read_first>
  - tests/conftest.py (created in task 0.7)
  - backend/app/main.py (created in task 0.5)
</read_first>
<action>
Create `tests/test_api.py` with:

```python
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
```
</action>
<acceptance_criteria>
- File `tests/test_api.py` exists
- File contains `class TestHealthEndpoint:`
- File contains `async def test_health_check_returns_healthy`
- File contains `class TestOpenAPIDocs:`
- File contains `async def test_openapi_json_accessible`
- File contains `assert response.status_code == 200`
</acceptance_criteria>
</task>
</tasks>

<verification>
## Wave 0 Verification

### Smoke Test
```bash
cd backend && pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov httpx
pytest tests/test_api.py -v
```

### Expected Output
- All tests pass
- Health endpoint returns `{"status": "healthy"}`
- OpenAPI JSON accessible at `/openapi.json`
- Swagger UI accessible at `/docs`

### Manual Verification
```bash
cd backend
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
# Visit http://localhost:8000/health
```
</verification>
