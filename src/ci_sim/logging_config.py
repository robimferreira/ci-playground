"""Logging for ci-sim"""

from __future__ import annotations

import contextvars
import logging
import logging.config
import os
import sys
from types import TracebackType
from typing import Final

from ci_sim import DIST_NAME, __version__

FORMATS: Final = frozenset({"json", "text"})

run_id_var: Final[contextvars.ContextVar[str]] = contextvars.ContextVar(
    "run_id", default="-"
)


class RunIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.run_id = run_id_var.get()
        return True


def setup_logging(level: str | None) -> None:
    """Configure root logger. Raises ValueError for an invalid level or format."""
    level_name: str = (level or os.getenv("LOG_LEVEL") or "WARNING").upper()
    if level_name not in logging.getLevelNamesMapping():
        raise ValueError(f"invalid log level: {level_name!r}")
    fmt: str = os.getenv("LOG_FORMAT") or "text"
    if fmt not in FORMATS:
        raise ValueError(
            f"invalid LOG_FORMAT: {fmt!r} (expected one of {sorted(FORMATS)})"
        )

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"run_id": {"()": RunIdFilter}},
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.json.JsonFormatter",
                    "fmt": "%(levelname)s %(name)s %(message)s",
                    "rename_fields": {"levelname": "level", "name": "logger"},
                    "timestamp": True,  # ISO-8601, UTC
                    "static_fields": {
                        "service": DIST_NAME,
                        "version": __version__,
                        "env": os.getenv("APP_ENV", "unknown"),
                    },
                },
                "text": {
                    "format": "%(asctime)s %(levelname)-8s %(name)s [%(run_id)s] %(message)s",
                },
            },
            "handlers": {
                "stderr": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",  # stdout is reserved for the tool's output
                    "formatter": fmt,
                    # on the handler, so records from every logger get it
                    "filters": ["run_id"],
                },
            },
            "root": {"level": level_name, "handlers": ["stderr"]},
        }
    )

    logging.captureWarnings(
        True
    )  # warnings.warn(...) -> the "py.warnings" logger
    sys.excepthook = (
        _log_uncaught  # crash becomes one CRITICAL record, not 20 journal lines
    )


def _log_uncaught(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: TracebackType | None,
) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return
    logging.getLogger(f"{__package__}.uncaught").critical(
        "unhandled exception", exc_info=(exc_type, exc_value, exc_tb)
    )
