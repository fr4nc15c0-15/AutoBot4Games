"""Retry utilities for transient automation failures.

Includes a generic decorator that retries operations with delay between attempts.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import TypeVar

from config.settings import DEFAULT_RETRY_DELAY

T = TypeVar("T")


def retry(attempts: int = 3, delay: float = DEFAULT_RETRY_DELAY):
    """Retry a callable when it raises, then re-raise with context.

    Args:
        attempts: Maximum number of tries.
        delay: Sleep delay between retries in seconds.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exc: Exception | None = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    # Keep the latest exception to preserve context if all attempts fail.
                    last_exc = exc
                    time.sleep(delay)
            raise RuntimeError(f"Retry exhausted for function: {func.__name__}") from last_exc

        return wrapper

    return decorator
