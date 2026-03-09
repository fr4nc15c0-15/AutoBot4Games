"""Memory cleanup utility functions.

Triggers Python garbage collection and logs system memory usage.
"""

from __future__ import annotations

import gc

import psutil

from utils.logger import get_logger

LOGGER = get_logger(__name__)


def free_memory() -> None:
    """Run garbage collection and log current virtual memory usage."""
    # Run Python object graph cleanup.
    gc.collect()

    # Log memory status for observability.
    memory = psutil.virtual_memory()
    LOGGER.info("Memory usage after cleanup: %.2f%%", memory.percent)
