from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistUpdate,
    WatchlistItemCreate,
    WatchlistItemBatchCreate,
    WatchlistResponse,
    WatchlistDetailResponse,
    WatchlistListResponse,
    MovieInWatchlist,
    PublicWatchlistResponse,
    PublicWatchlistDetailResponse,
)
from app.services.watchlist import watchlist_service


router = APIRouter(prefix="/watchlists", tags=["watchlists"])


@router.post("", response_model=WatchlistResponse)
async def create_watchlist(
    data: WatchlistCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new watchlist."""
    watchlist = await watchlist_service.create_watchlist(
        db, current_user.id, data.name, data.description, data.is_public
    )
    movie_count = await watchlist_service.get_movie_count(db, watchlist.id)
    return WatchlistResponse(
        id=watchlist.id,
        user_id=watchlist.user_id,
        name=watchlist.name,
        description=watchlist.description,
        is_public=watchlist.is_public,
        movie_count=movie_count,
        created_at=watchlist.created_at,
        updated_at=watchlist.updated_at,
    )


@router.get("", response_model=WatchlistListResponse)
async def list_watchlists(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's watchlists."""
    watchlists = await watchlist_service.get_user_watchlists(db, current_user.id)
    result = []
    for w in watchlists:
        movie_count = await watchlist_service.get_movie_count(db, w.id)
        result.append(WatchlistResponse(
            id=w.id,
            user_id=w.user_id,
            name=w.name,
            description=w.description,
            is_public=w.is_public,
            movie_count=movie_count,
            created_at=w.created_at,
            updated_at=w.updated_at,
        ))
    return WatchlistListResponse(watchlists=result, total=len(result))


@router.get("/{watchlist_id}", response_model=WatchlistDetailResponse)
async def get_watchlist(
    watchlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a watchlist by ID."""
    watchlist = await watchlist_service.get_watchlist(db, watchlist_id, current_user.id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    movies = [
        MovieInWatchlist(
            id=item.movie.id,
            title=item.movie.title,
            poster_url=item.movie.poster_url,
            position=item.position,
            added_at=item.created_at,
        )
        for item in sorted(watchlist.items, key=lambda x: x.position)
    ]

    return WatchlistDetailResponse(
        id=watchlist.id,
        user_id=watchlist.user_id,
        name=watchlist.name,
        description=watchlist.description,
        is_public=watchlist.is_public,
        created_at=watchlist.created_at,
        updated_at=watchlist.updated_at,
        movies=movies,
    )


@router.patch("/{watchlist_id}", response_model=WatchlistResponse)
async def update_watchlist(
    watchlist_id: int,
    data: WatchlistUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a watchlist."""
    watchlist = await watchlist_service.update_watchlist(
        db, watchlist_id, current_user.id, data.name, data.description, data.is_public
    )
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")

    movie_count = await watchlist_service.get_movie_count(db, watchlist.id)
    return WatchlistResponse(
        id=watchlist.id,
        user_id=watchlist.user_id,
        name=watchlist.name,
        description=watchlist.description,
        is_public=watchlist.is_public,
        movie_count=movie_count,
        created_at=watchlist.created_at,
        updated_at=watchlist.updated_at,
    )


@router.delete("/{watchlist_id}")
async def delete_watchlist(
    watchlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a watchlist."""
    deleted = await watchlist_service.delete_watchlist(db, watchlist_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    return {"message": "Watchlist deleted"}


@router.post("/{watchlist_id}/movies")
async def add_movie_to_watchlist(
    watchlist_id: int,
    data: WatchlistItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a movie to a watchlist."""
    item = await watchlist_service.add_movie_to_watchlist(
        db, watchlist_id, current_user.id, data.movie_id
    )
    if not item:
        raise HTTPException(status_code=404, detail="Watchlist not found or movie already in watchlist")
    return {"message": "Movie added to watchlist"}


@router.post("/{watchlist_id}/movies/batch")
async def add_movies_to_watchlist(
    watchlist_id: int,
    data: WatchlistItemBatchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add multiple movies to a watchlist."""
    added_count = 0
    for movie_id in data.movie_ids:
        item = await watchlist_service.add_movie_to_watchlist(
            db, watchlist_id, current_user.id, movie_id
        )
        if item:
            added_count += 1
    return {"message": f"Added {added_count} movies to watchlist"}


@router.delete("/{watchlist_id}/movies/{movie_id}")
async def remove_movie_from_watchlist(
    watchlist_id: int,
    movie_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a movie from a watchlist."""
    removed = await watchlist_service.remove_movie_from_watchlist(
        db, watchlist_id, current_user.id, movie_id
    )
    if not removed:
        raise HTTPException(status_code=404, detail="Watchlist or movie not found")
    return {"message": "Movie removed from watchlist"}


# Public watchlist endpoints
@router.get("/public", response_model=List[PublicWatchlistResponse])
async def list_public_watchlists(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Browse public watchlists."""
    watchlists = await watchlist_service.get_public_watchlists(db, skip, limit)
    result = []
    for w in watchlists:
        movie_count = await watchlist_service.get_movie_count(db, w.id)
        result.append(PublicWatchlistResponse(
            id=w.id,
            name=w.name,
            description=w.description,
            user_id=w.user_id,
            user_name=w.user.display_name if w.user else None,
            movie_count=movie_count,
            created_at=w.created_at,
        ))
    return result


@router.get("/{watchlist_id}/public", response_model=PublicWatchlistDetailResponse)
async def get_public_watchlist(
    watchlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a public watchlist by ID."""
    watchlist = await watchlist_service.get_public_watchlist(db, watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found or not public")

    movies = [
        MovieInWatchlist(
            id=item.movie.id,
            title=item.movie.title,
            poster_url=item.movie.poster_url,
            position=item.position,
            added_at=item.created_at,
        )
        for item in sorted(watchlist.items, key=lambda x: x.position)
    ]

    return PublicWatchlistDetailResponse(
        id=watchlist.id,
        name=watchlist.name,
        description=watchlist.description,
        user_id=watchlist.user_id,
        user_name=watchlist.user.display_name if watchlist.user else None,
        is_public=watchlist.is_public,
        created_at=watchlist.created_at,
        movies=movies,
    )
