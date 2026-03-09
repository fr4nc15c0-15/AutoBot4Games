"""Watchdog thread for crash/freeze recovery.

Monitors game process health and triggers restart flow when the process dies,
becomes unresponsive, or exceeds freeze timeout.
"""

from __future__ import annotations

import threading
import time

from config.settings import FREEZE_TIMEOUT_SECONDS, WATCHDOG_INTERVAL
from system.process_manager import is_process_running, kill_if_not_responding, restart_process
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class Watchdog(threading.Thread):
    """Background watchdog monitoring a single game process alias."""

    def __init__(self, process_name: str, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.process_name = process_name
        self.stop_event = stop_event
        self.last_healthy_timestamp = time.time()

    def run(self) -> None:
        """Continuously validate process health and recover as needed."""
        LOGGER.info("Watchdog started for '%s'", self.process_name)

        while not self.stop_event.is_set():
            if not is_process_running(self.process_name):
                LOGGER.warning("Process '%s' not detected; restarting", self.process_name)
                restart_process(self.process_name)
                self.last_healthy_timestamp = time.time()
            else:
                # Attempt to kill known dead states; restart if kill happened.
                killed = kill_if_not_responding(self.process_name)
                if killed:
                    LOGGER.warning("Process '%s' was unresponsive; restarting", self.process_name)
                    restart_process(self.process_name)
                self.last_healthy_timestamp = time.time()

            # Extra timeout safeguard for long stalls.
            if time.time() - self.last_healthy_timestamp > FREEZE_TIMEOUT_SECONDS:
                LOGGER.error("Freeze timeout exceeded for '%s'; forcing restart", self.process_name)
                restart_process(self.process_name)
                self.last_healthy_timestamp = time.time()

            time.sleep(WATCHDOG_INTERVAL)

        LOGGER.info("Watchdog stopped for '%s'", self.process_name)
