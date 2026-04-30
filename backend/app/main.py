from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
import os
import time
import logging

from app.config import settings
from app.database import engine, Base
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import (
    SecurityHeadersMiddleware,
    HTTPSRedirectMiddleware,
)
from app.middleware.tenant import TenantMiddleware
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.user import router as user_router
from app.routes.recommendations import router as recommendations_router
from app.routes.trending import router as trending_router
from app.routes.ratings import router as ratings_router
from app.routes.reviews import router as reviews_router
from app.routes.comments import router as comments_router
from app.routes.helpful_votes import router as helpful_votes_router
from app.routes.follows import router as follows_router
from app.routes.feed import router as feed_router
from app.routes.notifications import router as notifications_router
from app.routes.watchlist import router as watchlist_router
from app.routes.reports import router as reports_router
from app.routes.blocks import router as blocks_router
from app.routes.analytics import router as analytics_router
from app.routes.admin_metrics import router as admin_metrics_router
from app.routes.admin_dashboard import router as admin_dashboard_router
from app.routes.social_analytics import router as social_analytics_router
from app.routes.rec_insights import router as rec_insights_router
from app.routes.personalization import router as personalization_router
from app.routes.hls import router as hls_router
from app.routes.tenant_admin import router as tenant_admin_router
from app.routes.branding import router as branding_router
from app.routes.platform_admin import router as platform_admin_router
from app.routes.tenant_config import router as tenant_config_router
from app.routes.ai_editing import router as ai_editing_router
from app.routes.content_analytics import router as content_analytics_router
from app.routes.user_behavior import router as user_behavior_router
from app.routes.revenue import router as revenue_router
from app.routes.predictions import router as predictions_router
from app.routes.custom_reports import router as custom_reports_router
from app.routes.security import router as security_router
from app.routes.marketplace import router as marketplace_router
from app.routes.monetization import router as monetization_router
from app.routes.integrations import router as integrations_router
from app.routes.syndication import router as syndication_router
from app.routes.partner import router as partner_router
from app.routes.livestream import router as livestream_router
from app.routes.video_features import router as video_features_router
from app.routes.audio_features import router as audio_features_router
from app.routes.audio_track import router as audio_track_router
from app.routes.content_protection import router as content_protection_router
from app.routes.mobile import router as mobile_router
from app.routes.forum import router as forum_router
from app.routes.group import router as group_router
from app.routes.watch_party import router as watch_party_router
from app.routes.social_feed import router as social_feed_router
from app.routes.gamification import router as gamification_router
from app.routes.drm import router as drm_router
from app.routes.watermark import router as watermark_router
from app.routes.geo import router as geo_router
from app.routes.access import router as access_router
from app.routes.encryption import router as encryption_router
from app.routes.cdn import router as cdn_router
from app.routes.db_metrics import router as db_metrics_router
from app.routes.api_consolidation import router as api_consolidation_router
from app.routes.batch import router as batch_router
from app.routes.data_migration import router as data_migration_router
from app.routes.api_metrics import router as api_metrics_router
from app.routes.performance_tuning import router as performance_tuning_router
from app.routes.graphql import graphql_router
from app.routes.technical_debt import router as technical_debt_router
from app.routes.websocket import router as websocket_router
from app.routes.v5_foundation import router as v5_foundation_router
from app.routes.service_discovery import router as service_discovery_router
from app.routes.api_stability import router as api_stability_router
from app.routes.feature_freeze import router as feature_freeze_router
from app.routes.beta_readiness import router as beta_readiness_router
from app.routes.performance_validation import router as performance_validation_router
from app.routes.release_documentation import router as release_documentation_router
from app.routes.multi_tenant import router as multi_tenant_router
from app.routes.hdr_streaming import router as hdr_streaming_router
from app.routes.watch_party_v2 import router as watch_party_v2_router
from app.routes.ai_discovery import router as ai_discovery_router
from app.routes.enterprise_security import router as enterprise_security_router
from app.routes.events import router as events_router
from app.routes.version import router as version_router
from app.routes.health_detailed import router as health_detailed_router
from app.routes.incidents import router as incidents_router
from app.routes.chaos import router as chaos_router
from app.routes.feature_flags import router as feature_flags_router
from app.routes.capacity import router as capacity_router
from app.routes.sync import router as sync_router
from app.routes.creator import router as creator_router
from app.routes.video_tools import router as video_tools_router
from app.routes.live_stream import router as live_stream_router
from app.routes.content_workflow import router as content_workflow_router
from app.routes.rights import router as rights_router
from app.middleware.query_monitor import init_query_monitor
from app.middleware.tracing import TracingMiddleware
from app.middleware.versioning import VersioningMiddleware
from fastapi.middleware.gzip import GZipMiddleware

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        if process_time > 0.2:
            logger.warning(
                f"Slow request: {request.method} {request.url.path} took {process_time:.3f}s"
            )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    init_query_monitor(engine, slow_query_threshold=0.5)
    yield


app = FastAPI(
    title="CC Video API",
    description="Backend API for CC Video streaming platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SecurityHeadersMiddleware)
# app.add_middleware(HTTPSRedirectMiddleware)  # Disabled for local testing
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TenantMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(TracingMiddleware)
app.add_middleware(VersioningMiddleware, default_version="v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(recommendations_router)
app.include_router(trending_router)
app.include_router(ratings_router)
app.include_router(reviews_router)
app.include_router(comments_router)
app.include_router(helpful_votes_router)
app.include_router(follows_router)
app.include_router(feed_router)
app.include_router(notifications_router)
app.include_router(watchlist_router)
app.include_router(reports_router)
app.include_router(blocks_router)
app.include_router(analytics_router)
app.include_router(admin_metrics_router)
app.include_router(admin_dashboard_router)
app.include_router(social_analytics_router)
app.include_router(personalization_router)
app.include_router(rec_insights_router)
app.include_router(hls_router)
app.include_router(tenant_admin_router)
app.include_router(branding_router)
app.include_router(platform_admin_router)
app.include_router(tenant_config_router)
app.include_router(ai_editing_router)
app.include_router(content_analytics_router)
app.include_router(user_behavior_router)
app.include_router(revenue_router)
app.include_router(predictions_router)
app.include_router(custom_reports_router)
app.include_router(security_router)
app.include_router(marketplace_router)
app.include_router(monetization_router)
app.include_router(integrations_router)
app.include_router(syndication_router)
app.include_router(partner_router)
app.include_router(livestream_router)
app.include_router(video_features_router)
app.include_router(audio_features_router)
app.include_router(audio_track_router)
app.include_router(content_protection_router)
app.include_router(mobile_router)
app.include_router(forum_router)
app.include_router(group_router)
app.include_router(watch_party_router)
app.include_router(social_feed_router)
app.include_router(gamification_router)
app.include_router(drm_router)
app.include_router(watermark_router)
app.include_router(geo_router)
app.include_router(access_router)
app.include_router(encryption_router)
app.include_router(cdn_router)
app.include_router(db_metrics_router)
app.include_router(batch_router)
app.include_router(api_metrics_router)
app.include_router(graphql_router)
app.include_router(websocket_router)
app.include_router(service_discovery_router)
app.include_router(events_router)
app.include_router(version_router)
app.include_router(health_detailed_router)
app.include_router(incidents_router)
app.include_router(chaos_router)
app.include_router(feature_flags_router)
app.include_router(capacity_router)
app.include_router(sync_router)
app.include_router(creator_router)
app.include_router(video_tools_router)
app.include_router(live_stream_router)
app.include_router(content_workflow_router)
app.include_router(rights_router)
app.include_router(api_consolidation_router)
app.include_router(data_migration_router)
app.include_router(performance_tuning_router)
app.include_router(technical_debt_router)
app.include_router(v5_foundation_router)
app.include_router(feature_freeze_router)
app.include_router(beta_readiness_router)
app.include_router(performance_validation_router)
app.include_router(release_documentation_router)
app.include_router(multi_tenant_router)
app.include_router(hdr_streaming_router)
app.include_router(watch_party_v2_router)
app.include_router(ai_discovery_router)
app.include_router(enterprise_security_router)
app.include_router(api_stability_router)

posters_dir = os.path.join(settings.UPLOAD_DIR, "posters")
subtitles_dir = os.path.join(settings.UPLOAD_DIR, "subtitles")
logos_dir = os.path.join(settings.UPLOAD_DIR, "logos")
favicons_dir = os.path.join(settings.UPLOAD_DIR, "favicons")
os.makedirs(posters_dir, exist_ok=True)
os.makedirs(subtitles_dir, exist_ok=True)
os.makedirs(logos_dir, exist_ok=True)
os.makedirs(favicons_dir, exist_ok=True)

app.mount("/uploads/posters", StaticFiles(directory=posters_dir), name="posters")
app.mount("/uploads/subtitles", StaticFiles(directory=subtitles_dir), name="subtitles")
app.mount("/uploads/logos", StaticFiles(directory=logos_dir), name="logos")
app.mount("/uploads/favicons", StaticFiles(directory=favicons_dir), name="favicons")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "cc-video-api",
        "version": "1.0.0",
    }


@app.get("/healthz")
async def liveness():
    return {"status": "alive"}


@app.get("/readyz")
async def readiness():
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {"status": "not ready", "error": str(e)}, 503
