"""Retry helpers for robust automation operations.

This module implements a decorator for retrying transient failures.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from config.settings import DEFAULT_RETRY_DELAY

T = TypeVar("T")


def retry(attempts: int = 3, delay: float = DEFAULT_RETRY_DELAY):
    """Retry a function call multiple times before re-raising the error."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exc: Exception | None = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last_exc = exc
                    time.sleep(delay)
            raise RuntimeError(f"Retry failed for {func.__name__}") from last_exc

        return wrapper

    return decorator
