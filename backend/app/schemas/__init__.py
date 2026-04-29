from app.schemas.user import UserBase, UserCreate, UserResponse
from app.schemas.token import Token, TokenPayload
from app.schemas.video_file import VideoFileResponse
from app.schemas.movie import MovieBase, MovieCreate, MovieResponse, MovieListResponse

# Rebuild MovieResponse to resolve forward reference to VideoFileResponse
MovieResponse.model_rebuild()

__all__ = [
    "UserBase", "UserCreate", "UserResponse",
    "Token", "TokenPayload",
    "MovieBase", "MovieCreate", "MovieResponse", "MovieListResponse",
    "VideoFileResponse",
]
