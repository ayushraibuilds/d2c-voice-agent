"""
Structured logging for D2C Voice-First Agent.

Provides JSON-formatted structured logs with request correlation IDs,
replacing all ad-hoc print() statements.
"""

import logging
import sys
import uuid
from contextvars import ContextVar

# Context var for request correlation
_request_id: ContextVar[str] = ContextVar("request_id", default="no-request")


def get_request_id() -> str:
    return _request_id.get()


def set_request_id(request_id: str | None = None) -> str:
    rid = request_id or str(uuid.uuid4())[:8]
    _request_id.set(rid)
    return rid


class StructuredFormatter(logging.Formatter):
    """JSON-ish structured log formatter with correlation ID."""

    def format(self, record: logging.LogRecord) -> str:
        request_id = get_request_id()
        level = record.levelname
        module = record.module
        message = record.getMessage()

        # Include extra fields if present
        extras = ""
        if hasattr(record, "extra_data"):
            extras = f" | {record.extra_data}"

        return f"[{level}] [{request_id}] [{module}] {message}{extras}"


def setup_logger(name: str = "d2c_agent", level: str = "INFO") -> logging.Logger:
    """Create and configure a structured logger."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)

    return logger


# Module-level default logger
_logger: logging.Logger | None = None


def get_logger() -> logging.Logger:
    """Return the singleton application logger."""
    global _logger
    if _logger is None:
        from config import get_settings
        _logger = setup_logger(level=get_settings().log_level)
    return _logger


def log_with_extras(level: str, message: str, **kwargs):
    """Log a message with optional structured key-value extras."""
    logger = get_logger()
    record_method = getattr(logger, level.lower(), logger.info)
    if kwargs:
        extra_str = " ".join(f"{k}={v}" for k, v in kwargs.items())
        record_method(message, extra={"extra_data": extra_str})
    else:
        record_method(message)
