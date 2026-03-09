"""Centralized logging utilities for GameAutomationBot.

Provides a configured logger with stream and rotating-file handlers.
The log format includes severity, timestamp, module name, and message.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from config.paths import LOGS_DIR

# Ensure log directory exists before handlers are created.
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Create or return a configured logger instance.

    Args:
        name: Logger name, typically `__name__` of caller module.

    Returns:
        A logger with both console and rotating file output.
    """
    logger = logging.getLogger(name)

    # Guard against duplicate handlers when modules are imported repeatedly.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s | %(name)s | %(message)s")

    # Console output for real-time monitoring.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Rotating file output for historical diagnostics.
    file_handler = RotatingFileHandler(
        LOGS_DIR / "automation.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
