from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.analytics import AnalyticsResponse, ActivityTimelineResponse, ExportDataResponse
from app.services.analytics import analytics_service
import json
import csv
import io

router = APIRouter(prefix="/api", tags=["analytics"])


@router.get("/users/me/analytics", response_model=AnalyticsResponse)
async def get_analytics(
    refresh: bool = Query(False, description="Force refresh analytics"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's analytics dashboard data."""
    data = await analytics_service.get_user_analytics(db, current_user.id, force_refresh=refresh)
    return AnalyticsResponse(**data)


@router.get("/users/me/analytics/watch-time")
async def get_watch_time(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get watch time statistics only."""
    data = await analytics_service.get_user_analytics(db, current_user.id)
    return data["watch_time"]


@router.get("/users/me/analytics/genres")
async def get_genre_breakdown(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get genre preferences breakdown."""
    data = await analytics_service.get_user_analytics(db, current_user.id)
    return data["genre_breakdown"]


@router.get("/users/me/analytics/patterns")
async def get_time_patterns(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get viewing time patterns."""
    data = await analytics_service.get_user_analytics(db, current_user.id)
    return {
        "hourly": data["hourly_pattern"],
        "daily": data["daily_pattern"]
    }


@router.get("/users/me/analytics/timeline", response_model=ActivityTimelineResponse)
async def get_activity_timeline(
    activity_type: str = Query(None, description="Filter by activity type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's activity timeline."""
    activities = await analytics_service.get_activity_timeline(
        db, current_user.id, activity_type, skip, limit
    )
    return ActivityTimelineResponse(
        activities=activities,
        total=len(activities)
    )


@router.get("/users/me/analytics/export")
async def export_analytics(
    format: str = Query("json", description="Export format: json or csv"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Export user's viewing data."""
    data = await analytics_service.export_user_data(db, current_user.id)
    
    if format == "csv":
        # Generate CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["Movie Title", "Movie ID", "Watched At", "Completed"])
        
        # Write data
        for item in data["watch_history"]:
            writer.writerow([
                item["movie_title"],
                item["movie_id"],
                item["watched_at"],
                item["completed"]
            ])
        
        output.seek(0)
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=viewing_history_{current_user.id}.csv"
            }
        )
    else:
        # Return JSON
        return JSONResponse(
            content=data,
            headers={
                "Content-Disposition": f"attachment; filename=viewing_data_{current_user.id}.json"
            }
        )
