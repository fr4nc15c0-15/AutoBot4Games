"""Simple timing helpers used by detection and recovery code."""

from __future__ import annotations

import time


def now() -> float:
    """Return current UNIX timestamp in seconds."""
    return time.time()


def elapsed(start_timestamp: float) -> float:
    """Return elapsed seconds since a start timestamp."""
    return time.time() - start_timestamp
