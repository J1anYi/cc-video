from typing import List
from pydantic import BaseModel
from app.schemas.movie import MovieResponse


class TrendingMovie(BaseModel):
    movie: MovieResponse
    view_count: int


class TrendingResponse(BaseModel):
    movies: List[TrendingMovie]


class RelatedMoviesResponse(BaseModel):
    movies: List[MovieResponse]
