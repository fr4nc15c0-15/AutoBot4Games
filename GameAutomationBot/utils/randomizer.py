"""Randomization helpers used across human-like action routines.

This module wraps common random value generators for readability.
"""

from __future__ import annotations

import random


def rand_float(minimum: float, maximum: float) -> float:
    """Return a random float in inclusive range."""
    return random.uniform(minimum, maximum)


def rand_int(minimum: int, maximum: int) -> int:
    """Return a random integer in inclusive range."""
    return random.randint(minimum, maximum)
