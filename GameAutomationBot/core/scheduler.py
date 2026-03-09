"""Background scheduler thread for periodic tasks.

This lightweight scheduler executes timed callables while the bot runs.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from config.settings import SCHEDULER_INTERVAL
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class Scheduler(threading.Thread):
    """Periodic scheduler for non-critical recurring jobs."""

    def __init__(self, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.stop_event = stop_event
        self.jobs: list[tuple[Callable[[], None], float, float]] = []

    def add_job(self, callback: Callable[[], None], interval: float) -> None:
        """Register a callback with a recurring interval in seconds."""
        self.jobs.append((callback, interval, 0.0))

    def run(self) -> None:
        """Main scheduler loop that dispatches jobs based on elapsed time."""
        LOGGER.info("Scheduler started")
        while not self.stop_event.is_set():
            now = time.time()
            updated_jobs = []
            for callback, interval, last_run in self.jobs:
                if now - last_run >= interval:
                    try:
                        callback()
                    except Exception as exc:  # noqa: BLE001
                        LOGGER.exception("Scheduler job failed: %s", exc)
                    last_run = now
                updated_jobs.append((callback, interval, last_run))
            self.jobs = updated_jobs
            time.sleep(SCHEDULER_INTERVAL)
        LOGGER.info("Scheduler stopped")
