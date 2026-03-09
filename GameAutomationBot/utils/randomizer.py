"""Randomization helper functions used to humanize bot behavior."""

from __future__ import annotations

import random


def rand_float(min_value: float, max_value: float) -> float:
    """Return random float from [min_value, max_value]."""
    return random.uniform(min_value, max_value)


def rand_int(min_value: int, max_value: int) -> int:
    """Return random integer from [min_value, max_value]."""
    return random.randint(min_value, max_value)
