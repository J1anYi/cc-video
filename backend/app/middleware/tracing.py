from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import logging
from datetime import datetime
from typing import Optional
import json

logger = logging.getLogger(__name__)


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or propagate request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        span_id = str(uuid.uuid4())
        parent_span_id = request.headers.get("X-Span-ID")

        # Store in request state
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        request.state.parent_span_id = parent_span_id

        # Start span
        start_time = datetime.utcnow()

        # Process request
        response = await call_next(request)

        # End span
        end_time = datetime.utcnow()
        duration_ms = (end_time - start_time).total_seconds() * 1000

        # Add tracing headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Span-ID"] = span_id

        # Log span
        span_data = {
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "operation": f"{request.method} {request.url.path}",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_ms": round(duration_ms, 2),
            "status_code": response.status_code,
            "service": "cc-video-api",
        }

        logger.info(f"Span: {json.dumps(span_data)}")

        return response


def get_trace_context(request: Request) -> dict:
    """Extract trace context from request for downstream calls."""
    return {
        "X-Request-ID": getattr(request.state, "request_id", str(uuid.uuid4())),
        "X-Trace-ID": getattr(request.state, "trace_id", str(uuid.uuid4())),
        "X-Span-ID": str(uuid.uuid4()),
        "X-Parent-Span-ID": getattr(request.state, "span_id", ""),
    }


class Span:
    """Helper class for creating child spans."""

    def __init__(self, name: str, trace_id: str, parent_span_id: Optional[str] = None):
        self.name = name
        self.trace_id = trace_id
        self.span_id = str(uuid.uuid4())
        self.parent_span_id = parent_span_id
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def start(self):
        self.start_time = datetime.utcnow()

    def end(self):
        self.end_time = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": (
                (self.end_time - self.start_time).total_seconds() * 1000
                if self.start_time and self.end_time
                else None
            ),
        }
