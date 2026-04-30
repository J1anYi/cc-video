---
wave: 2
depends_on:
  - wave-0
  - wave-1
files_modified:
  - backend/app/services/__init__.py
  - backend/app/services/auth.py
  - backend/app/services/user.py
  - backend/app/routes/__init__.py
  - backend/app/routes/auth.py
  - backend/app/dependencies.py
  - backend/app/main.py
  - tests/test_auth.py
requirements_addressed:
  - AUTH-01
  - AUTH-02
  - AUTH-03
autonomous: true
---

# Wave 2: Authentication Endpoints

<objective>
Implement JWT-based authentication with login, logout, refresh, and current-user endpoints. Use httpOnly cookies for refresh tokens and return access tokens in response bodies. Enable session persistence across browser refresh.
</objective>

<must_haves>
- Login endpoint (POST /auth/login) that validates credentials and returns access token + sets refresh cookie
- Logout endpoint (POST /auth/logout) that clears refresh cookie
- Refresh endpoint (POST /auth/refresh) that issues new access token from refresh cookie
- Current user endpoint (GET /auth/me) that returns authenticated user profile
- AuthService for password hashing and token creation/verification
- UserService for user lookup
- get_current_user dependency for protected routes
</must_haves>

<tasks>
<task id="2.1">
<name>Create AuthService for password and JWT handling</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pattern 2: JWT Token Service)
  - backend/app/config.py (settings from Wave 0)
  - backend/app/schemas/token.py (TokenPayload from Wave 1)
</read_first>
<action>
Create `backend/app/services/__init__.py` with:
```python
from app.services.auth import auth_service
from app.services.user import user_service

__all__ = ["auth_service", "user_service"]
```

Create `backend/app/services/auth.py` with:
```python
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.schemas.token import TokenPayload


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, subject: str, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {
            "sub": subject,
            "role": role,
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        to_encode = {
            "sub": subject,
            "exp": expire,
            "type": "refresh"
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[TokenPayload]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except JWTError:
            return None


auth_service = AuthService()
```
</action>
<acceptance_criteria>
- File `backend/app/services/auth.py` exists
- File contains `class AuthService:`
- File contains `def verify_password(self, plain_password: str, hashed_password: str) -> bool`
- File contains `def get_password_hash(self, password: str) -> str`
- File contains `def create_access_token(self, subject: str, role: str) -> str`
- File contains `def create_refresh_token(self, subject: str) -> str`
- File contains `def decode_token(self, token: str) -> Optional[TokenPayload]`
- File contains `auth_service = AuthService()`
</acceptance_criteria>
</task>

<task id="2.2">
<name>Create UserService for user CRUD operations</name>
<read_first>
  - backend/app/models/user.py (User model from Wave 1)
  - backend/app/services/auth.py (auth_service from task 2.1)
</read_first>
<action>
Create `backend/app/services/user.py` with:
```python
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.services.auth import auth_service


class UserService:
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, email: str, password: str, role: UserRole = UserRole.USER) -> User:
        hashed_password = auth_service.get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user_service = UserService()
```
</action>
<acceptance_criteria>
- File `backend/app/services/user.py` exists
- File contains `class UserService:`
- File contains `async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]`
- File contains `async def get_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]`
- File contains `async def create(self, db: AsyncSession, email: str, password: str, role: UserRole = UserRole.USER) -> User`
- File contains `user_service = UserService()`
</acceptance_criteria>
</task>

<task id="2.3">
<name>Implement get_current_user dependency</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pattern 3: Current User Dependency)
  - backend/app/dependencies.py (existing file from Wave 0)
  - backend/app/services/auth.py (auth_service from task 2.1)
  - backend/app/services/user.py (user_service from task 2.2)
</read_first>
<action>
Update `backend/app/dependencies.py` to:
```python
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.user import User
from app.services.auth import auth_service
from app.services.user import user_service


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    
    if payload is None or payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await user_service.get_by_id(db, int(payload.sub))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive",
        )
    
    return user
```
</action>
<acceptance_criteria>
- File `backend/app/dependencies.py` contains `from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials`
- File contains `security = HTTPBearer()`
- File contains `async def get_current_user(...) -> User:`
- File contains `credentials: HTTPAuthorizationCredentials = Depends(security)`
- File contains `if payload is None or payload.type != "access":`
- File contains `raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED`
</acceptance_criteria>
</task>

<task id="2.4">
<name>Create authentication routes (login, logout, refresh, me)</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pattern 5, 6, 7, 8)
  - backend/app/services/auth.py (auth_service from task 2.1)
  - backend/app/services/user.py (user_service from task 2.2)
  - backend/app/dependencies.py (get_current_user from task 2.3)
  - backend/app/schemas/user.py (UserResponse from Wave 1)
  - backend/app/schemas/token.py (Token from Wave 1)
</read_first>
<action>
Create `backend/app/routes/__init__.py` with:
```python
from app.routes.auth import router as auth_router

__all__ = ["auth_router"]
```

Create `backend/app/routes/auth.py` with:
```python
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.token import Token
from app.services.auth import auth_service
from app.services.user import user_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Login with email and password. Returns access token and sets refresh token cookie."""
    user = await user_service.get_by_email(db, form_data.username)
    
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )
    
    access_token = auth_service.create_access_token(str(user.id), user.role.value)
    refresh_token = auth_service.create_refresh_token(str(user.id))
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Logout by clearing the refresh token cookie."""
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Refresh access token using refresh token from cookie."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not refresh_token:
        raise credentials_exception
    
    payload = auth_service.decode_token(refresh_token)
    
    if payload is None or payload.type != "refresh":
        raise credentials_exception
    
    user = await user_service.get_by_id(db, int(payload.sub))
    
    if not user:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )
    
    access_token = auth_service.create_access_token(str(user.id), user.role.value)
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get the currently authenticated user's profile."""
    return UserResponse.model_validate(current_user)
```
</action>
<acceptance_criteria>
- File `backend/app/routes/auth.py` exists
- File contains `router = APIRouter(prefix="/auth", tags=["auth"])`
- File contains `@router.post("/login", response_model=Token)`
- File contains `@router.post("/logout")`
- File contains `@router.post("/refresh", response_model=Token)`
- File contains `@router.get("/me", response_model=UserResponse)`
- File contains `response.set_cookie(key="refresh_token", httponly=True, secure=True, samesite="lax")`
- File contains `response.delete_cookie(key="refresh_token")`
</acceptance_criteria>
</task>

<task id="2.5">
<name>Register auth router in main application</name>
<read_first>
  - backend/app/main.py (from Wave 0)
  - backend/app/routes/auth.py (router from task 2.4)
</read_first>
<action>
Update `backend/app/main.py` to include the auth router. Add after the CORS middleware setup:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routes.auth import router as auth_router


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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```
</action>
<acceptance_criteria>
- File `backend/app/main.py` contains `from app.routes.auth import router as auth_router`
- File contains `app.include_router(auth_router)`
</acceptance_criteria>
</task>

<task id="2.6">
<name>Create authentication endpoint tests</name>
<read_first>
  - tests/conftest.py (fixtures from Wave 0)
  - backend/app/routes/auth.py (auth routes from task 2.4)
  - backend/app/services/user.py (user_service from task 2.2)
</read_first>
<action>
Create `tests/test_auth.py` with:
```python
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
        
        assert response.status_code == 403
    
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
```
</action>
<acceptance_criteria>
- File `tests/test_auth.py` exists
- File contains `class TestLoginEndpoint:` with `test_login_success`, `test_login_sets_refresh_cookie`, `test_login_invalid_password`, `test_login_invalid_email`
- File contains `class TestLogoutEndpoint:` with `test_logout_clears_cookie`
- File contains `class TestRefreshEndpoint:` with `test_refresh_token_success`, `test_refresh_without_cookie`, `test_refresh_with_invalid_token`
- File contains `class TestMeEndpoint:` with `test_me_with_valid_token`, `test_me_without_token`, `test_me_with_invalid_token`, `test_me_admin_user`
</acceptance_criteria>
</task>
</tasks>

<verification>
## Wave 2 Verification

### Run Auth Tests
```bash
pytest tests/test_auth.py -v
```

### Expected Output
- All login tests pass
- Login returns access token and sets refresh cookie
- Logout clears refresh cookie
- Refresh issues new access token
- Me endpoint returns user profile
- Invalid tokens are rejected

### Manual API Test
```bash
cd backend
# Create .env with SECRET_KEY
echo "SECRET_KEY=$(openssl rand -hex 32)" > .env

uvicorn app.main:app --reload

# Test login (need to create user first via script or direct DB)
# Visit http://localhost:8000/docs for interactive testing
```

### Token Flow Verification
1. POST /auth/login with form data → get access_token
2. GET /auth/me with Bearer token → get user profile
3. POST /auth/refresh with refresh_token cookie → get new access_token
4. POST /auth/logout → clears cookie
</verification>
