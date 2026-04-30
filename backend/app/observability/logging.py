import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class LogContext:
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


class StructuredFormatter(logging.Formatter):
    def __init__(self, context: LogContext = None):
        super().__init__()
        self.context = context or LogContext()

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add context
        if self.context.trace_id:
            log_data["trace_id"] = self.context.trace_id
        if self.context.span_id:
            log_data["span_id"] = self.context.span_id
        if self.context.request_id:
            log_data["request_id"] = self.context.request_id
        if self.context.user_id:
            log_data["user_id"] = self.context.user_id
        if self.context.tenant_id:
            log_data["tenant_id"] = self.context.tenant_id

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class StructuredLogger:
    def __init__(self, name: str, context: LogContext = None):
        self.logger = logging.getLogger(name)
        self.context = context or LogContext()
        self._setup_handler()

    def _setup_handler(self):
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(StructuredFormatter(self.context))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def update_context(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)

    def _log(self, level: int, message: str, extra: Dict[str, Any] = None):
        record = self.logger.makeRecord(
            self.logger.name,
            level,
            "",
            0,
            message,
            (),
            None,
        )
        if extra:
            record.extra_data = extra
        self.logger.handle(record)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, kwargs if kwargs else None)

    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, kwargs if kwargs else None)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, kwargs if kwargs else None)

    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, kwargs if kwargs else None)

    def with_context(self, **kwargs) -> "StructuredLogger":
        new_context = LogContext(
            trace_id=kwargs.get("trace_id", self.context.trace_id),
            span_id=kwargs.get("span_id", self.context.span_id),
            request_id=kwargs.get("request_id", self.context.request_id),
            user_id=kwargs.get("user_id", self.context.user_id),
            tenant_id=kwargs.get("tenant_id", self.context.tenant_id),
        )
        return StructuredLogger(self.logger.name, new_context)


def get_logger(name: str, **context) -> StructuredLogger:
    return StructuredLogger(name, LogContext(**context))
