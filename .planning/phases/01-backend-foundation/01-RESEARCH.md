# Phase 1: Backend Foundation - Research

**Researched:** 2026-04-29
**Domain:** FastAPI backend with SQLite, JWT authentication, RBAC
**Confidence:** HIGH

## Summary

This phase establishes the foundational backend API for a video streaming platform with separated frontend/backend architecture. The core challenge is implementing secure JWT-based authentication with refresh tokens that persist sessions across browser refreshes, while enforcing admin-only access through RBAC middleware. SQLite provides zero-config development storage with SQLAlchemy ORM offering a clean migration path to PostgreSQL for production.

**Primary recommendation:** Use FastAPI's native dependency injection for both authentication and RBAC enforcement, combined with aiosqlite for async SQLite operations. Implement refresh tokens as httpOnly cookies with access tokens returned in response bodies for frontend storage in memory.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Use **FastAPI** as the backend framework
- **D-02:** Use **SQLite** for development with **SQLAlchemy** ORM
- **D-03:** Use **JWT tokens** with httpOnly cookies for authentication
- **D-04:** Implement **access token + refresh token** pattern
- **D-05:** Implement **role-based access control (RBAC)** middleware
- **D-06:** Use **FastAPI's auto-generated OpenAPI/Swagger UI**
- **D-07:** Use **src/ layout** with clear module separation

### Claude's Discretion
- Specific library versions and minor implementation details
- Error response format standardization
- Logging configuration
- Environment variable naming conventions

### Deferred Ideas (OUT OF SCOPE)
None - discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AUTH-01 | User can log in with valid credentials before accessing movie pages | JWT authentication endpoints (login, logout, current-user) |
| AUTH-02 | User session persists across browser refresh until logout or expiration | Refresh token pattern with httpOnly cookies |
| AUTH-03 | User can log out from the web app | Logout endpoint with token invalidation |
| AUTH-04 | Administrator access is restricted to users with an admin role | RBAC middleware with role checking |
| API-01 | Frontend communicates with backend through documented HTTP APIs | FastAPI OpenAPI/Swagger auto-generation |
| API-02 | Backend persists users, roles, movies, and uploaded video file metadata | SQLAlchemy models with SQLite |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| User authentication | API / Backend | - | Auth logic, token generation, and verification belong server-side |
| Session management | API / Backend | Browser / Client | Backend issues and validates tokens; client stores tokens securely |
| Role enforcement | API / Backend | - | RBAC must be enforced server-side; client-side checks are UX only |
| User persistence | Database / Storage | - | SQLite database stores user accounts and roles |
| API documentation | API / Backend | - | FastAPI auto-generates OpenAPI spec from route definitions |
| Token storage | Browser / Client | - | Access token in memory; refresh token in httpOnly cookie |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| fastapi | 0.115.x | Web framework | Async-first, automatic OpenAPI docs, strong typing with Pydantic [CITED: fastapi.tiangolo.com] |
| uvicorn | 0.34.x | ASGI server | Standard FastAPI server with excellent performance [VERIFIED: PyPI] |
| sqlalchemy | 2.0.x | ORM | Database-agnostic with async support, migration via Alembic [CITED: sqlalchemy.org] |
| aiosqlite | 0.21.x | Async SQLite driver | Enables async SQLite operations with SQLAlchemy 2.0 [VERIFIED: PyPI] |
| python-jose | 3.3.x | JWT handling | Industry standard for JWT encoding/decoding with RS256/HS256 [VERIFIED: PyPI] |
| passlib | 1.7.x | Password hashing | bcrypt wrapper for secure password storage [VERIFIED: PyPI] |
| pydantic | 2.x | Data validation | FastAPI's native validation layer, eliminates manual validation code [CITED: docs.pydantic.dev] |
| pydantic-settings | 2.x | Settings management | Environment variable loading with type coercion [CITED: docs.pydantic.dev] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| alembic | 1.13.x | Database migrations | Any schema changes after initial setup |
| python-multipart | 0.0.x | Form parsing | Required for OAuth2PasswordRequestForm (login) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| python-jose | pyjwt | jose supports more algorithms; pyjwt is lighter but requires more manual work |
| passlib[bcrypt] | argon2-cffi | argon2 is newer but bcrypt has more battle-testing; passlib abstracts the choice |
| SQLite | PostgreSQL | SQLite is zero-config for dev; PostgreSQL needed for production scaling [ASSUMED] |

**Installation:**

```bash
# Core dependencies
pip install fastapi uvicorn[standard] sqlalchemy aiosqlite

# Authentication
pip install python-jose[cryptography] passlib[bcrypt]

# Validation and settings
pip install pydantic pydantic-settings

# Migrations
pip install alembic

# Form parsing for OAuth2 login
pip install python-multipart
```

**Version verification:**

```bash
pip show fastapi uvicorn sqlalchemy aiosqlite python-jose passlib pydantic pydantic-settings alembic python-multipart
```

[ASSUMED] Versions based on current stable releases as of 2026-04. Verify against PyPI before pinning.

## Architecture Patterns

### System Architecture Diagram

```
+---------------------------------------------------------------------+
|                           Browser / Client                           |
|  +-----------------+    +------------------+    +----------------+  |
|  |  Access Token   |    |  Refresh Token   |    |   User State   |  |
|  |  (in memory)    |    |  (httpOnly cookie)|    |                |  |
|  +--------+--------+    +--------+---------+    +----------------+  |
+-----------+---------------------+-----------------------------------+
            |                     |
            | Authorization:      | Cookie: refresh_token
            | Bearer <access>     |
            v                     v
+---------------------------------------------------------------------+
|                        FastAPI Backend                               |
|  +-------------------------------------------------------------+    |
|  |                    Middleware Layer                          |    |
|  |  CORS  |  Auth Dependencies  |  RBAC Enforcement            |    |
|  +---------------------+---------------------------------------+    |
|                        |                                            |
|  +---------------------v---------------------------------------+    |
|  |                    Route Layer                               |    |
|  |  /auth/login  |  /auth/logout  |  /auth/me  |  /admin/*     |    |
|  +---------------------+---------------------------------------+    |
|                        |                                            |
|  +---------------------v---------------------------------------+    |
|  |                   Service Layer                              |    |
|  |  AuthService  |  UserService  |  TokenService               |    |
|  +---------------------+---------------------------------------+    |
|                        |                                            |
|  +---------------------v---------------------------------------+    |
|  |                   Data Access Layer                          |    |
|  |  SQLAlchemy ORM  |  AsyncSession  |  Repository Pattern      |    |
|  +---------------------+---------------------------------------+    |
+------------------------+--------------------------------------------+
                         |
                         v
+---------------------------------------------------------------------+
|                     SQLite Database                                  |
|  Tables: users, roles, movies, video_files                          |
|  File: backend/data/cc_video.db                                      |
+---------------------------------------------------------------------+
```

### Recommended Project Structure

```
backend/
+-- app/
|   +-- __init__.py
|   +-- main.py              # FastAPI app instance, CORS, middleware
|   +-- config.py            # Pydantic Settings for env vars
|   +-- database.py          # SQLAlchemy async engine, session factory
|   +-- dependencies.py      # Shared dependencies (get_db, get_current_user)
|   +-- models/              # SQLAlchemy ORM models
|   |   +-- __init__.py
|   |   +-- user.py          # User model with role field
|   |   +-- movie.py         # Movie model
|   |   +-- video_file.py    # Video file metadata model
|   +-- schemas/             # Pydantic schemas for request/response
|   |   +-- __init__.py
|   |   +-- user.py          # UserCreate, UserResponse, UserLogin
|   |   +-- token.py         # Token, TokenPayload
|   |   +-- movie.py         # MovieCreate, MovieResponse
|   +-- routes/              # API route handlers
|   |   +-- __init__.py
|   |   +-- auth.py          # Login, logout, refresh, me endpoints
|   |   +-- admin.py         # Admin-only endpoints (Phase 2)
|   +-- services/            # Business logic
|   |   +-- __init__.py
|   |   +-- auth.py          # Token creation, verification
|   |   +-- user.py          # User CRUD operations
|   +-- middleware/          # Custom middleware
|       +-- __init__.py
|       +-- rbac.py          # Role-based access control
+-- alembic/                 # Database migrations
|   +-- versions/
|   +-- env.py
+-- alembic.ini
+-- data/                    # SQLite database files
|   +-- cc_video.db
+-- tests/                   # Test suite
|   +-- __init__.py
|   +-- conftest.py          # Fixtures
|   +-- test_auth.py         # Auth endpoint tests
|   +-- test_rbac.py         # RBAC enforcement tests
+-- requirements.txt
+-- pyproject.toml           # Optional: modern Python packaging
```

### Pattern 1: Async Database Session with Dependency Injection

**What:** Use FastAPI's dependency injection to provide async database sessions to route handlers, ensuring proper cleanup.

**When to use:** Every route that needs database access.

**Example:**

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,  # "sqlite+aiosqlite:///./data/cc_video.db"
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

# app/dependencies.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

[Source: Pattern derived from FastAPI documentation patterns and SQLAlchemy 2.0 async guide]

### Pattern 2: JWT Token Service

**What:** Centralized service for creating and verifying JWT access and refresh tokens.

**When to use:** Login, token refresh, and authenticated endpoint access.

**Example:**

```python
# app/services/auth.py
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

[Source: Pattern derived from OWASP recommendations and FastAPI security best practices]

### Pattern 3: Current User Dependency

**What:** Dependency that extracts and validates the JWT from the Authorization header, returning the current user or raising 401.

**When to use:** Any endpoint requiring authentication.

**Example:**

```python
# app/dependencies.py (extended)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.auth import auth_service

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
    
    result = await db.execute(select(User).where(User.id == int(payload.sub)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user
```

[Source: FastAPI security documentation pattern]

### Pattern 4: RBAC Enforcement Dependency

**What:** Dependency factory that checks if the current user has the required role(s).

**When to use:** Admin-only endpoints (AUTH-04).

**Example:**

```python
# app/middleware/rbac.py
from typing import List
from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.user import User

def require_roles(allowed_roles: List[str]):
    """Dependency factory for role-based access control."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    return role_checker

# Usage in routes:
# @router.post("/admin/movies", dependencies=[Depends(require_roles(["admin"]))])
# async def create_movie(...):
#     ...
```

[Source: FastAPI dependency injection pattern for authorization]

### Pattern 5: Login Endpoint with httpOnly Cookie

**What:** Login endpoint that returns access token in response body and sets refresh token as httpOnly cookie.

**When to use:** User authentication (AUTH-01).

**Example:**

```python
# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.token import Token
from app.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    # Find user by username (email)
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Create tokens
    access_token = auth_service.create_access_token(str(user.id), user.role)
    refresh_token = auth_service.create_refresh_token(str(user.id))
    
    # Set refresh token as httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 days
    )
    
    return Token(access_token=access_token, token_type="bearer")
```

[Source: OWASP session management recommendations and FastAPI cookie patterns]

### Pattern 6: Token Refresh Endpoint

**What:** Endpoint that validates the refresh token from httpOnly cookie and issues a new access token.

**When to use:** Session persistence across browser refresh (AUTH-02).

**Example:**

```python
# app/routes/auth.py (extended)
from fastapi import Cookie

@router.post("/refresh", response_model=Token)
async def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> Token:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )
    
    payload = auth_service.decode_token(refresh_token)
    
    if payload is None or payload.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Verify user still exists and is active
    result = await db.execute(
        select(User).where(User.id == int(payload.sub))
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    # Issue new access token
    access_token = auth_service.create_access_token(str(user.id), user.role)
    
    return Token(access_token=access_token, token_type="bearer")
```

[Source: JWT refresh token best practices]

### Pattern 7: Logout Endpoint

**What:** Endpoint that clears the refresh token cookie.

**When to use:** User logout (AUTH-03).

**Example:**

```python
# app/routes/auth.py (extended)
@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}
```

### Pattern 8: Current User Endpoint

**What:** Endpoint that returns the currently authenticated user's profile.

**When to use:** Frontend needs to display user info or verify authentication state.

**Example:**

```python
# app/routes/auth.py (extended)
from app.dependencies import get_current_user
from app.schemas.user import UserResponse

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)
```

### Anti-Patterns to Avoid

- **Storing access tokens in localStorage or non-httpOnly cookies:** XSS vulnerability allows token theft. Store access tokens in memory only.
- **Using synchronous SQLAlchemy with FastAPI:** Blocks the event loop. Use `aiosqlite` driver and async sessions.
- **Storing refresh tokens in database without rotation:** If refresh token is stolen, attacker has persistent access. Consider rotating refresh tokens on each use. [ASSUMED - token rotation is an enhancement]
- **Rolling your own crypto:** Never write custom encryption, hashing, or token logic. Use `python-jose`, `passlib`, and established libraries.
- **Hardcoding secret keys:** Use environment variables via `pydantic-settings`. Rotate keys periodically.
- **Skipping CORS configuration:** Frontend and backend are on different ports in development. Configure CORS properly.
- **Returning sensitive data in user responses:** Never return password hashes or internal IDs in API responses.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Password hashing | Custom hash function | passlib[bcrypt] | Timing attacks, salt management, algorithm updates |
| JWT creation/verification | Manual encoding | python-jose | Cryptographic correctness, standard compliance |
| Request validation | Manual if/else chains | Pydantic | Type coercion, clear error messages, OpenAPI schema generation |
| Database migrations | Manual SQL scripts | Alembic | Version tracking, rollback support, team coordination |
| Auth token handling | Custom middleware | FastAPI Depends + HTTPBearer | Testable, documented, integrated with OpenAPI |
| Settings management | os.environ everywhere | pydantic-settings | Type coercion, validation, .env file support |

**Key insight:** FastAPI's ecosystem provides production-ready components for auth, validation, and database access. Custom implementations introduce subtle bugs and security vulnerabilities.

## Common Pitfalls

### Pitfall 1: Sync SQLite Driver with Async FastAPI

**What goes wrong:** Using `sqlite://` (synchronous driver) with async SQLAlchemy blocks the event loop, causing performance issues and potential deadlocks under load.

**Why it happens:** Developers copy connection strings from older tutorials or don't realize SQLAlchemy 2.0 requires the async driver explicitly.

**How to avoid:** Use `sqlite+aiosqlite://` connection string and install `aiosqlite` package.

**Warning signs:** Requests take longer than expected, `RuntimeWarning: coroutine was never awaited` errors.

### Pitfall 2: Refresh Token Not Persisting

**What goes wrong:** User is logged out when refreshing the browser despite "remember me" being checked.

**Why it happens:** Refresh token cookie was set without `secure`, `samesite`, or `httponly` flags, or the cookie domain/path doesn't match.

**How to avoid:** Always set `httponly=True`, `secure=True` (production), `samesite="lax"` on refresh token cookies. Test cookie behavior in the target browser.

**Warning signs:** Cookies not visible in browser DevTools Application tab, cookies sent on some requests but not others.

### Pitfall 3: Missing CORS Headers

**What goes wrong:** Frontend (port 5173) cannot call backend API (port 8000) due to CORS errors.

**Why it happens:** FastAPI doesn't include CORS middleware by default, and separated frontend/backend run on different origins during development.

**How to avoid:** Add `CORSMiddleware` with appropriate `allow_origins`, `allow_credentials=True`, and required methods/headers.

**Warning signs:** Browser console shows "CORS policy" errors, preflight OPTIONS requests fail.

### Pitfall 4: JWT Secret Key in Code

**What goes wrong:** Secret key is hardcoded in source code, committed to git, and visible to anyone with repository access.

**Why it happens:** Convenience during initial development, forgot to move to environment variables.

**How to avoid:** Use `pydantic-settings` to load `SECRET_KEY` from environment variable. Generate a strong random key with `openssl rand -hex 32`. Add `.env` to `.gitignore`.

**Warning signs:** Secret key visible in source code, environment variable fallback to hardcoded value.

### Pitfall 5: Admin Role Checked in Frontend Only

**What goes wrong:** Non-admin users can access admin endpoints by directly calling the API, bypassing frontend role checks.

**Why it happens:** Developer implemented role-based UI hiding but forgot server-side enforcement.

**How to avoid:** Always enforce roles server-side using RBAC middleware/dependency. Frontend hiding is UX, not security.

**Warning signs:** Admin routes lack `Depends(require_roles(["admin"]))`, only frontend hides admin buttons.

### Pitfall 6: Alembic Not Configured for Async

**What goes wrong:** Migrations fail or run synchronously despite async SQLAlchemy setup.

**Why it happens:** Alembic configuration defaults to synchronous engine.

**How to avoid:** Configure `alembic/env.py` to use async engine and `run_migrations_online` with async connection.

**Warning signs:** Migration commands hang or error with async-related messages.

## Code Examples

### Complete User Model

```python
# app/models/user.py
from datetime import datetime
from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### Movie and Video File Models

```python
# app/models/movie.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

class PublicationStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DISABLED = "disabled"

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    publication_status: Mapped[PublicationStatus] = mapped_column(
        Enum(PublicationStatus), default=PublicationStatus.DRAFT, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to video files
    video_files: Mapped[list["VideoFile"]] = relationship("VideoFile", back_populates="movie")

# app/models/video_file.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class VideoFile(Base):
    __tablename__ = "video_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)  # bytes
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    movie: Mapped["Movie"] = relationship("Movie", back_populates="video_files")
```

### Pydantic Schemas

```python
# app/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)

# app/schemas/token.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str  # "access" or "refresh"
    role: Optional[str] = None
```

### FastAPI Main Application

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routes import auth, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (for dev; use Alembic in production)
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
    allow_origins=settings.CORS_ORIGINS,  # ["http://localhost:5173"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Configuration with Pydantic Settings

```python
# app/config.py
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CC Video"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/cc_video.db"
    
    # Authentication
    SECRET_KEY: str  # Required, no default
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

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| SQLAlchemy 1.4 sync | SQLAlchemy 2.0 async | 2023 | Native async/await support, better type hints |
| Pydantic v1 | Pydantic v2 | 2023 | 5-50x faster validation, `model_validate` instead of `parse_obj` |
| Manual CORS | CORSMiddleware | FastAPI 0.x | Declarative CORS configuration |
| Storing tokens in localStorage | httpOnly cookies + in-memory access | OWASP 2020s | XSS protection for refresh tokens |

**Deprecated/outdated:**
- `SQLAlchemy` synchronous session with `sqlite://`: Use `aiosqlite` driver with async sessions
- `orm_mode` in Pydantic v2: Use `from_attributes = True` instead

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | SQLite is sufficient for v1 development and will migrate to PostgreSQL for production | Standard Stack | May need earlier PostgreSQL if SQLite limitations impact features |
| A2 | Refresh token rotation is an enhancement, not required for v1 | Pattern 2 | May need to implement rotation if security requirements increase |
| A3 | bcrypt is acceptable; argon2 is newer but bcrypt has more battle-testing | Standard Stack | May need to switch to argon2 if security audit requires it |
| A4 | Package versions are current stable releases as of 2026-04 | Standard Stack | Version numbers may be stale; verify against PyPI before pinning |

## Open Questions

1. **Should refresh tokens be stored in database for revocation?**
   - What we know: JWT refresh tokens are stateless but cannot be revoked without server-side tracking.
   - What's unclear: Is revocation needed for v1? (e.g., admin bans user, password change)
   - Recommendation: Start stateless. Add database tracking if revocation scenarios emerge.

2. **Should admin users also have user capabilities, or are they separate roles?**
   - What we know: RBAC will enforce admin-only endpoints.
   - What's unclear: Can an admin also browse movies as a user?
   - Recommendation: Admins should have both roles or access to all functionality. Single `role` field with admin superpowers is simpler.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.10+ | Backend runtime | Unknown | - | - |
| pip | Package management | Unknown | - | - |
| SQLite | Database | Unknown | - | Built-in with Python |

**Missing dependencies with no fallback:**
- Python 3.10+ (required for modern async syntax and type hints)

**Missing dependencies with fallback:**
- None identified

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest with pytest-asyncio |
| Config file | pytest.ini or pyproject.toml |
| Quick run command | `pytest tests/ -v --tb=short -x` |
| Full suite command | `pytest tests/ -v --cov=app --cov-report=term-missing` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AUTH-01 | User login with valid credentials | unit + integration | `pytest tests/test_auth.py::test_login_success -x` | Wave 0 |
| AUTH-01 | User login rejected with invalid credentials | unit | `pytest tests/test_auth.py::test_login_invalid_password -x` | Wave 0 |
| AUTH-02 | Refresh token issues new access token | unit | `pytest tests/test_auth.py::test_refresh_token -x` | Wave 0 |
| AUTH-03 | Logout clears refresh token cookie | unit | `pytest tests/test_auth.py::test_logout -x` | Wave 0 |
| AUTH-04 | Non-admin rejected from admin endpoints | unit | `pytest tests/test_rbac.py::test_admin_required -x` | Wave 0 |
| AUTH-04 | Admin can access admin endpoints | unit | `pytest tests/test_rbac.py::test_admin_allowed -x` | Wave 0 |
| API-01 | OpenAPI documentation accessible | smoke | `pytest tests/test_api.py::test_openapi_docs -x` | Wave 0 |
| API-02 | User model persists to database | unit | `pytest tests/test_models.py::test_user_creation -x` | Wave 0 |
| API-02 | Movie model persists to database | unit | `pytest tests/test_models.py::test_movie_creation -x` | Wave 0 |
| API-02 | VideoFile model persists to database | unit | `pytest tests/test_models.py::test_video_file_creation -x` | Wave 0 |

### Sampling Rate

- **Per task commit:** `pytest tests/ -v --tb=short -x`
- **Per wave merge:** `pytest tests/ -v --cov=app --cov-report=term-missing`
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps

- [ ] `tests/conftest.py` - Shared fixtures (test client, async session, test user)
- [ ] `tests/test_auth.py` - Authentication endpoint tests
- [ ] `tests/test_rbac.py` - RBAC enforcement tests
- [ ] `tests/test_models.py` - Database model tests
- [ ] `tests/test_api.py` - API documentation smoke tests
- [ ] Framework install: `pip install pytest pytest-asyncio pytest-cov httpx` - Required for async test support

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | yes | JWT with httpOnly cookies, passlib/bcrypt |
| V3 Session Management | yes | Refresh token pattern, secure cookie flags |
| V4 Access Control | yes | RBAC dependency injection |
| V5 Input Validation | yes | Pydantic schemas |
| V6 Cryptography | yes | python-jose for JWT, bcrypt for passwords |

### Known Threat Patterns for FastAPI + JWT

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| XSS token theft | Information Disclosure | httpOnly cookies for refresh tokens, access tokens in memory only |
| CSRF token use | Tampering | SameSite cookie attribute, validate origin headers |
| JWT algorithm confusion | Tampering | Explicitly whitelist allowed algorithms (HS256, RS256) |
| Brute force login | Denial of Service | Rate limiting (not in v1 scope, document for future) |
| Session fixation | Spoofing | Issue new tokens on authentication, invalidate old sessions |

## Sources

### Primary (HIGH confidence)
- FastAPI documentation (fastapi.tiangolo.com) - security, dependencies, database patterns [CITED]
- SQLAlchemy 2.0 documentation (docs.sqlalchemy.org) - async configuration [CITED]
- OWASP Authentication Cheat Sheet (cheatsheetseries.owasp.org) - session management, token storage [CITED]
- Pydantic v2 documentation - model validation, settings management [CITED]

### Secondary (MEDIUM confidence)
- Python package registry (PyPI) - package availability and versions [VERIFIED]

### Tertiary (LOW confidence)
- Web search results - patterns validated against primary sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Based on official documentation and verified package availability
- Architecture: HIGH - Following established FastAPI patterns with clear separation of concerns
- Pitfalls: HIGH - Common issues documented in community resources and official guides

**Research date:** 2026-04-29
**Valid until:** 90 days - stable framework patterns, verify package versions before implementation
