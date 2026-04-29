---
wave: 1
depends_on:
  - wave-0
files_modified:
  - backend/app/models/__init__.py
  - backend/app/models/user.py
  - backend/app/models/movie.py
  - backend/app/models/video_file.py
  - backend/app/schemas/__init__.py
  - backend/app/schemas/user.py
  - backend/app/schemas/token.py
  - backend/app/schemas/movie.py
  - tests/test_models.py
requirements_addressed:
  - API-02
autonomous: true
---

# Wave 1: Database Models

<objective>
Create SQLAlchemy ORM models for User, Role, Movie, and VideoFile with proper relationships. Define Pydantic schemas for request/response validation. Ensure all models can persist to the SQLite database.
</objective>

<must_haves>
- User model with id, email, hashed_password, role, is_active, timestamps
- Movie model with id, title, description, publication_status, timestamps
- VideoFile model with id, movie_id (FK), filename, file_path, file_size, mime_type, duration, timestamps
- UserRole enum with USER and ADMIN values
- PublicationStatus enum with DRAFT, PUBLISHED, DISABLED values
- Pydantic schemas for User (create, response) and Token (access, payload)
- Tests verifying all models can be created and persisted
</must_haves>

<tasks>
<task id="1.1">
<name>Create User model with role enum</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Complete User Model code example)
  - backend/app/database.py (Base class definition from Wave 0)
</read_first>
<action>
Create `backend/app/models/__init__.py` with:
```python
from app.models.user import User, UserRole
from app.models.movie import Movie, PublicationStatus
from app.models.video_file import VideoFile

__all__ = ["User", "UserRole", "Movie", "PublicationStatus", "VideoFile"]
```

Create `backend/app/models/user.py` with:
```python
from datetime import datetime
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
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
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```
</action>
<acceptance_criteria>
- File `backend/app/models/user.py` exists
- File contains `class UserRole(str, enum.Enum):` with `USER = "user"` and `ADMIN = "admin"`
- File contains `class User(Base):`
- File contains `__tablename__ = "users"`
- File contains `id: Mapped[int] = mapped_column(primary_key=True`
- File contains `email: Mapped[str] = mapped_column(String(255), unique=True`
- File contains `role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole)`
- File contains `is_active: Mapped[bool]`
- File `backend/app/models/__init__.py` exists and exports User, UserRole
</acceptance_criteria>
</task>

<task id="1.2">
<name>Create Movie model with publication status enum</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Movie and Video File Models code example)
  - backend/app/database.py (Base class definition)
  - backend/app/models/user.py (pattern for enum and model from task 1.1)
</read_first>
<action>
Create `backend/app/models/movie.py` with:
```python
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

if TYPE_CHECKING:
    from app.models.video_file import VideoFile


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
        SQLEnum(PublicationStatus), default=PublicationStatus.DRAFT, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to video files
    video_files: Mapped[list["VideoFile"]] = relationship("VideoFile", back_populates="movie")
```
</action>
<acceptance_criteria>
- File `backend/app/models/movie.py` exists
- File contains `class PublicationStatus(str, enum.Enum):` with DRAFT, PUBLISHED, DISABLED
- File contains `class Movie(Base):`
- File contains `__tablename__ = "movies"`
- File contains `title: Mapped[str]`
- File contains `description: Mapped[Optional[str]]`
- File contains `publication_status: Mapped[PublicationStatus]`
- File contains `video_files: Mapped[list["VideoFile"]] = relationship`
- File `backend/app/models/__init__.py` exports Movie, PublicationStatus
</acceptance_criteria>
</task>

<task id="1.3">
<name>Create VideoFile model with movie relationship</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Movie and Video File Models code example)
  - backend/app/database.py (Base class definition)
  - backend/app/models/movie.py (relationship pattern from task 1.2)
</read_first>
<action>
Create `backend/app/models/video_file.py` with:
```python
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie


class VideoFile(Base):
    __tablename__ = "video_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    movie: Mapped["Movie"] = relationship("Movie", back_populates="video_files")
```
</action>
<acceptance_criteria>
- File `backend/app/models/video_file.py` exists
- File contains `class VideoFile(Base):`
- File contains `__tablename__ = "video_files"`
- File contains `movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id")`
- File contains `filename: Mapped[str]`
- File contains `file_path: Mapped[str]`
- File contains `file_size: Mapped[int] = mapped_column(BigInteger`
- File contains `mime_type: Mapped[str]`
- File contains `movie: Mapped["Movie"] = relationship("Movie", back_populates="video_files")`
- File `backend/app/models/__init__.py` exports VideoFile
</acceptance_criteria>
</task>

<task id="1.4">
<name>Create Pydantic schemas for User</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pydantic Schemas code example)
  - backend/app/models/user.py (UserRole enum from task 1.1)
</read_first>
<action>
Create `backend/app/schemas/__init__.py` with:
```python
from app.schemas.user import UserBase, UserCreate, UserResponse
from app.schemas.token import Token, TokenPayload
from app.schemas.movie import MovieBase, MovieCreate, MovieResponse

__all__ = [
    "UserBase", "UserCreate", "UserResponse",
    "Token", "TokenPayload",
    "MovieBase", "MovieCreate", "MovieResponse",
]
```

Create `backend/app/schemas/user.py` with:
```python
from datetime import datetime
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
        from_attributes = True
```
</action>
<acceptance_criteria>
- File `backend/app/schemas/user.py` exists
- File contains `class UserBase(BaseModel):` with `email: EmailStr`
- File contains `class UserCreate(UserBase):` with `password: str`
- File contains `class UserResponse(UserBase):` with `id`, `role`, `is_active`, `created_at`
- File contains `from_attributes = True`
- File `backend/app/schemas/__init__.py` exists and exports UserBase, UserCreate, UserResponse
</acceptance_criteria>
</task>

<task id="1.5">
<name>Create Pydantic schemas for Token</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pydantic Schemas code example)
</read_first>
<action>
Create `backend/app/schemas/token.py` with:
```python
from typing import Optional
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
</action>
<acceptance_criteria>
- File `backend/app/schemas/token.py` exists
- File contains `class Token(BaseModel):` with `access_token: str` and `token_type: str = "bearer"`
- File contains `class TokenPayload(BaseModel):` with `sub`, `exp`, `type`, `role`
- File `backend/app/schemas/__init__.py` exports Token, TokenPayload
</acceptance_criteria>
</task>

<task id="1.6">
<name>Create Pydantic schemas for Movie</name>
<read_first>
  - .planning/phases/01-backend-foundation/01-RESEARCH.md (Pydantic Schemas code example)
  - backend/app/models/movie.py (PublicationStatus enum from task 1.2)
</read_first>
<action>
Create `backend/app/schemas/movie.py` with:
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.movie import PublicationStatus


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None


class MovieCreate(MovieBase):
    publication_status: PublicationStatus = PublicationStatus.DRAFT


class MovieResponse(MovieBase):
    id: int
    publication_status: PublicationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```
</action>
<acceptance_criteria>
- File `backend/app/schemas/movie.py` exists
- File contains `class MovieBase(BaseModel):` with `title` and `description`
- File contains `class MovieCreate(MovieBase):` with `publication_status`
- File contains `class MovieResponse(MovieBase):` with `id`, `publication_status`, `created_at`, `updated_at`
- File contains `from_attributes = True`
- File `backend/app/schemas/__init__.py` exports MovieBase, MovieCreate, MovieResponse
</acceptance_criteria>
</task>

<task id="1.7">
<name>Create model persistence tests</name>
<read_first>
  - tests/conftest.py (fixtures from Wave 0)
  - backend/app/models/user.py (User model from task 1.1)
  - backend/app/models/movie.py (Movie model from task 1.2)
  - backend/app/models/video_file.py (VideoFile model from task 1.3)
</read_first>
<action>
Create `tests/test_models.py` with:
```python
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
```
</action>
<acceptance_criteria>
- File `tests/test_models.py` exists
- File contains `class TestUserModel:`
- File contains `async def test_create_user` and `async def test_create_admin_user`
- File contains `class TestMovieModel:`
- File contains `async def test_create_movie` and `async def test_movie_published_status`
- File contains `class TestVideoFileModel:`
- File contains `async def test_create_video_file` and `async def test_video_file_relationship`
</acceptance_criteria>
</task>
</tasks>

<verification>
## Wave 1 Verification

### Run Model Tests
```bash
pytest tests/test_models.py -v
```

### Expected Output
- All tests pass
- User can be created with USER and ADMIN roles
- Movie can be created with DRAFT, PUBLISHED, DISABLED statuses
- VideoFile can be created and linked to Movie
- Relationship between VideoFile and Movie works

### Database Inspection (manual)
```bash
cd backend
uvicorn app.main:app --reload
# Tables should be auto-created on startup
# Check with: sqlite3 data/cc_video.db ".tables"
```
</verification>
