"""System memory management helpers.

This module exposes lightweight memory cleanup operations between bot runs.
"""

from __future__ import annotations

import gc

import psutil

from utils.logger import get_logger

LOGGER = get_logger(__name__)


def free_memory() -> None:
    """Trigger Python garbage collection and log memory usage stats."""
    gc.collect()
    mem = psutil.virtual_memory()
    LOGGER.info("Memory usage after cleanup: %.2f%%", mem.percent)
