from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(UserBase):
    id: int
    display_name: str | None = None
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    display_name: str | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class PublicProfileResponse(BaseModel):
    id: int
    display_name: str | None
    followers_count: int
    following_count: int
    review_count: int
    rating_count: int

    class Config:
        from_attributes = True


class UserAdminView(BaseModel):
    """Full user details for admin view."""
    id: int
    email: str
    display_name: str | None = None
    role: UserRole
    is_active: bool
    is_suspended: bool
    deleted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Paginated user list response."""
    users: list[UserAdminView]
    total: int
    page: int
    limit: int
    total_pages: int


class UserSuspensionRequest(BaseModel):
    """Request to suspend or unsuspend a user."""
    suspend: bool
