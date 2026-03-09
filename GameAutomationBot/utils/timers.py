"""Timing utilities for delay and timeout calculations.

This module centralizes helpers for elapsed-time checks.
"""

from __future__ import annotations

import time


def now() -> float:
    """Return current unix timestamp in seconds."""
    return time.time()


def elapsed(start_ts: float) -> float:
    """Return elapsed seconds since given start timestamp."""
    return time.time() - start_ts
