"""Process watchdog for freeze/crash detection and automatic recovery.

The watchdog monitors process responsiveness and triggers restart routines.
"""

from __future__ import annotations

import threading
import time

from config.settings import FREEZE_TIMEOUT_SECONDS, WATCHDOG_INTERVAL
from system.process_manager import is_process_running, kill_if_not_responding, restart_process
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class Watchdog(threading.Thread):
    """Background thread that keeps the game process healthy."""

    def __init__(self, process_name: str, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.process_name = process_name
        self.stop_event = stop_event
        self.last_alive = time.time()

    def run(self) -> None:
        """Continuously monitor game process and restart when unhealthy."""
        LOGGER.info("Watchdog started for %s", self.process_name)
        while not self.stop_event.is_set():
            if not is_process_running(self.process_name):
                LOGGER.warning("Process %s not running; attempting restart", self.process_name)
                restart_process(self.process_name)
                self.last_alive = time.time()
            else:
                unresponsive = kill_if_not_responding(self.process_name)
                if unresponsive:
                    LOGGER.warning("Process %s unresponsive; restarting", self.process_name)
                    restart_process(self.process_name)
                    self.last_alive = time.time()
                else:
                    self.last_alive = time.time()

            if time.time() - self.last_alive > FREEZE_TIMEOUT_SECONDS:
                LOGGER.error("Freeze timeout exceeded for %s; forcing restart", self.process_name)
                restart_process(self.process_name)
                self.last_alive = time.time()

            time.sleep(WATCHDOG_INTERVAL)
        LOGGER.info("Watchdog stopped for %s", self.process_name)
