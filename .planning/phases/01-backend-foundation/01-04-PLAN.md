---
wave: 3
depends_on:
  - wave-0
  - wave-1
  - wave-2
files_modified:
  - backend/app/middleware/__init__.py
  - backend/app/middleware/rbac.py
  - backend/app/routes/admin.py
  - backend/app/main.py
  - tests/test_rbac.py
requirements_addressed:
  - AUTH-04
autonomous: true
---

# Wave 3: RBAC Middleware and Admin Routes

<objective>
Implement role-based access control (RBAC) middleware that enforces admin-only access to protected endpoints. Create admin route scaffold for Phase 2. Verify that non-admin users are rejected from admin endpoints.
</objective>

<must_haves>
- RBAC dependency factory (require_roles) that checks user role before allowing access
- Admin router with placeholder endpoints for Phase 2 (movie management)
- Admin endpoints protected by RBAC - reject non-admin users with 403 Forbidden
- Tests verifying admin can access admin endpoints, regular users cannot
</must_haves>

<tasks>
<task id="3.1">
<name>Create RBAC middleware dependency</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pattern 4: RBAC Enforcement Dependency)
  - backend/app/dependencies.py (get_current_user from Wave 2)
  - backend/app/models/user.py (User, UserRole from Wave 1)
</read_first>
<action>
Create `backend/app/middleware/__init__.py` with:
```python
from app.middleware.rbac import require_roles

__all__ = ["require_roles"]
```

Create `backend/app/middleware/rbac.py` with:
```python
from typing import List
from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.user import User


def require_roles(allowed_roles: List[str]):
    """Dependency factory for role-based access control.
    
    Usage:
        @router.post("/admin/endpoint", dependencies=[Depends(require_roles(["admin"]))])
        async def admin_endpoint():
            ...
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    
    return role_checker
```
</action>
<acceptance_criteria>
- File `backend/app/middleware/rbac.py` exists
- File contains `def require_roles(allowed_roles: List[str]):`
- File contains `async def role_checker(current_user: User = Depends(get_current_user)) -> User:`
- File contains `if current_user.role.value not in allowed_roles:`
- File contains `raise HTTPException(status_code=status.HTTP_403_FORBIDDEN`
- File `backend/app/middleware/__init__.py` exists and exports require_roles
</acceptance_criteria>
</task>

<task id="3.2">
<name>Create admin router with protected endpoints</name>
<read_first>
  - backend/app/middleware/rbac.py (require_roles from task 3.1)
  - backend/app/dependencies.py (get_current_user from Wave 2)
</read_first>
<action>
Create `backend/app/routes/admin.py` with:
```python
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
```
</action>
<acceptance_criteria>
- File `backend/app/routes/admin.py` exists
- File contains `router = APIRouter(prefix="/admin", tags=["admin"])`
- File contains `admin_required = Depends(require_roles(["admin"]))`
- File contains `@router.get("/users", dependencies=[admin_required])`
- File contains `@router.post("/movies", response_model=MovieResponse, dependencies=[admin_required])`
- File contains `@router.get("/movies", dependencies=[admin_required])`
- File contains `@router.get("/dashboard", dependencies=[admin_required])`
</acceptance_criteria>
</task>

<task id="3.3">
<name>Register admin router in main application</name>
<read_first>
  - backend/app/main.py (from Wave 2)
  - backend/app/routes/admin.py (router from task 3.2)
</read_first>
<action>
Update `backend/app/main.py` to include the admin router:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="CC Video API",
    description="Backend API for CC Video streaming platform",
    version="1.0.0",
    lifespan=lifespan,
)

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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```
</action>
<acceptance_criteria>
- File `backend/app/main.py` contains `from app.routes.admin import router as admin_router`
- File contains `app.include_router(admin_router)`
</acceptance_criteria>
</task>

<task id="3.4">
<name>Create RBAC enforcement tests</name>
<read_first>
  - tests/conftest.py (fixtures from Wave 0)
  - backend/app/routes/admin.py (admin routes from task 3.2)
  - backend/app/services/user.py (user_service from Wave 2)
  - backend/app/services/auth.py (auth_service from Wave 2)
</read_first>
<action>
Create `tests/test_rbac.py` with:
```python
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
        
        # Should be 403 (Forbidden) due to missing auth, not 401
        assert response.status_code == 403


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
```
</action>
<acceptance_criteria>
- File `tests/test_rbac.py` exists
- File contains `class TestAdminEndpoints:`
- File contains `async def test_admin_can_access_dashboard` and `test_admin_can_list_users` and `test_admin_can_create_movies`
- File contains `async def test_regular_user_cannot_access_dashboard` and `test_regular_user_cannot_list_users` and `test_regular_user_cannot_create_movies`
- File contains `async def test_unauthenticated_user_cannot_access_admin`
- File contains `class TestRoleChecking:` with role value tests
</acceptance_criteria>
</task>
</tasks>

<verification>
## Wave 3 Verification

### Run RBAC Tests
```bash
pytest tests/test_rbac.py -v
```

### Expected Output
- Admin user can access all admin endpoints
- Regular user receives 403 Forbidden on admin endpoints
- Unauthenticated user receives 403 on admin endpoints
- Role values are correctly checked

### Manual API Test
```bash
cd backend
uvicorn app.main:app --reload

# Create admin user via script or direct DB insertion
# Login as admin, get token
# Access /admin/dashboard with admin token -> 200 OK
# Access /admin/dashboard with regular user token -> 403 Forbidden
```

### OpenAPI Verification
Visit http://localhost:8000/docs and verify:
- Admin endpoints appear under "admin" tag
- Admin endpoints show lock icon (require authentication)
- Auth endpoints appear under "auth" tag
</verification>
