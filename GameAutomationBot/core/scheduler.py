"""Lightweight periodic scheduler thread.

The scheduler can register recurring jobs that run in the background at
user-defined intervals while automation workflows continue in the foreground.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from config.settings import SCHEDULER_INTERVAL
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class Scheduler(threading.Thread):
    """Background scheduler for periodic housekeeping tasks."""

    def __init__(self, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.stop_event = stop_event
        # Each job stores callback, interval, and last run timestamp.
        self._jobs: list[dict[str, float | Callable[[], None]]] = []

    def add_job(self, callback: Callable[[], None], interval_seconds: float) -> None:
        """Register a recurring callback."""
        self._jobs.append({"callback": callback, "interval": interval_seconds, "last": 0.0})

    def run(self) -> None:
        """Scheduler polling loop."""
        LOGGER.info("Scheduler started")
        while not self.stop_event.is_set():
            now = time.time()

            for job in self._jobs:
                callback = job["callback"]
                interval = float(job["interval"])
                last = float(job["last"])

                if now - last >= interval:
                    try:
                        callback()
                    except Exception as exc:  # noqa: BLE001
                        LOGGER.exception("Scheduled job failed: %s", exc)
                    finally:
                        # Update last-run timestamp even on failure to avoid hot-looping.
                        job["last"] = now

            time.sleep(SCHEDULER_INTERVAL)

        LOGGER.info("Scheduler stopped")
