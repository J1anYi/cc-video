from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
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


@router.post("/register", response_model=Token)
async def register(
    response: Response,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """Register a new user. Returns access token and sets refresh token cookie."""
    try:
        user = await user_service.create(db, user_data.email, user_data.password)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
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
