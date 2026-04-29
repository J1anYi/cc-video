"""Production logging configuration with structured output."""
import logging
import sys
import json
from datetime import datetime
from typing import Any

from app.config import settings


class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Includes timestamp, level, and additional context.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'service': 'cc-video-api',
            'environment': 'production' if not settings.DEBUG else 'development',
        }

        # Add request ID if available
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id

        # Add user ID if available
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        # Add extra fields
        if hasattr(record, 'http_method'):
            log_data['http_method'] = record.http_method
        if hasattr(record, 'http_path'):
            log_data['http_path'] = record.http_path
        if hasattr(record, 'http_status'):
            log_data['http_status'] = record.http_status
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class RequestIdFilter(logging.Filter):
    """
    Filter to add request ID to log records.
    Requires middleware to set request_id on the record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        # Default values
        if not hasattr(record, 'request_id'):
            record.request_id = '-'
        if not hasattr(record, 'user_id'):
            record.user_id = '-'
        return True


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)

    if settings.DEBUG:
        # Human-readable format for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        # JSON format for production
        formatter = JsonFormatter()

    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIdFilter())

    root_logger.addHandler(console_handler)

    # Set log levels for third-party libraries
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)


# Log level convenience functions
def log_request(logger: logging.Logger, method: str, path: str, status_code: int, duration_ms: float, **kwargs: Any) -> None:
    """Log an HTTP request with structured data."""
    logger.info(
        f"HTTP {method} {path}",
        extra={
            'http_method': method,
            'http_path': path,
            'http_status': status_code,
            'duration_ms': duration_ms,
            **kwargs
        }
    )


def log_error(logger: logging.Logger, error: Exception, context: dict = None, **kwargs: Any) -> None:
    """Log an error with context."""
    logger.error(
        f"Error: {type(error).__name__}: {str(error)}",
        extra={
            'error_type': type(error).__name__,
            'error_message': str(error),
            **(context or {}),
            **kwargs
        },
        exc_info=True
    )
