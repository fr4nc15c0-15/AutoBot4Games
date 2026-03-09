"""Core bot engine for lifecycle and background thread management.

This module provides a base class used by game-specific orchestrators.
"""

from __future__ import annotations

from threading import Event

from core.scheduler import Scheduler
from core.watchdog import Watchdog
from vision.popup_detector import PopupDetector
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class BotEngine:
    """Base game bot engine that owns popup detector, scheduler, and watchdog."""

    def __init__(self, process_name: str) -> None:
        self.process_name = process_name
        self.stop_event = Event()
        self.scheduler = Scheduler(self.stop_event)
        self.watchdog = Watchdog(process_name, self.stop_event)
        self.popup_detector = PopupDetector(self.stop_event)

    def start_services(self) -> None:
        """Start background services required for resilient automation."""
        LOGGER.info("Starting engine services for process: %s", self.process_name)
        self.scheduler.start()
        self.watchdog.start()
        self.popup_detector.start()

    def stop_services(self) -> None:
        """Stop all background services and wait for graceful shutdown."""
        LOGGER.info("Stopping engine services for process: %s", self.process_name)
        self.stop_event.set()
        self.scheduler.join(timeout=3)
        self.watchdog.join(timeout=3)
        self.popup_detector.join(timeout=3)
