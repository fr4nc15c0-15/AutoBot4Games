"""Application logging configuration.

This module creates console + file loggers and stores log files in logs/.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from config.paths import LOGS_DIR

LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with both stream and rotating file handlers."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s | %(name)s | %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(LOGS_DIR / "automation.log", maxBytes=2_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
