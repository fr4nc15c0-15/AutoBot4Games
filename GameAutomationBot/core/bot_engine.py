"""Base engine that powers game-specific bot orchestrators.

The engine provides:
- launch/bootstrap hooks
- background thread lifecycle management
- generic UI-failure auto-recovery workflow
"""

from __future__ import annotations

from threading import Event

from config.settings import MAX_RECOVERY_ATTEMPTS, MAX_UI_FAILURES_BEFORE_RECOVERY
from core.scheduler import Scheduler
from core.watchdog import Watchdog
from system.process_manager import restart_process
from utils.logger import get_logger
from vision.popup_detector import PopupDetector

LOGGER = get_logger(__name__)


class BotEngine:
    """Reusable base class for all game bot orchestrators."""

    def __init__(self, process_name: str) -> None:
        self.process_name = process_name
        self.stop_event = Event()

        # Background services.
        self.scheduler = Scheduler(self.stop_event)
        self.watchdog = Watchdog(process_name, self.stop_event)
        self.popup_detector = PopupDetector(self.stop_event)

        # UI recovery counters.
        self.ui_failures = 0
        self.recovery_attempts = 0

    def start_services(self) -> None:
        """Start scheduler, watchdog, and popup detector threads."""
        LOGGER.info("Starting services for '%s'", self.process_name)
        self.scheduler.start()
        self.watchdog.start()
        self.popup_detector.start()

    def stop_services(self) -> None:
        """Stop all background services cleanly."""
        LOGGER.info("Stopping services for '%s'", self.process_name)
        self.stop_event.set()
        self.scheduler.join(timeout=3)
        self.watchdog.join(timeout=3)
        self.popup_detector.join(timeout=3)

    def register_ui_failure(self, reason: str) -> None:
        """Track UI detection failures and trigger recovery when threshold reached."""
        self.ui_failures += 1
        LOGGER.warning("UI failure %s/%s for '%s': %s", self.ui_failures, MAX_UI_FAILURES_BEFORE_RECOVERY, self.process_name, reason)

        if self.ui_failures >= MAX_UI_FAILURES_BEFORE_RECOVERY:
            self.perform_recovery()

    def reset_ui_failures(self) -> None:
        """Reset UI failure counter after successful interaction."""
        self.ui_failures = 0

    def perform_recovery(self) -> None:
        """Run auto-recovery flow: retry state recovery or restart game process."""
        self.recovery_attempts += 1
        LOGGER.warning("Recovery attempt %s/%s for '%s'", self.recovery_attempts, MAX_RECOVERY_ATTEMPTS, self.process_name)

        if self.recovery_attempts < MAX_RECOVERY_ATTEMPTS:
            # Lightweight recovery path: allow game logic to continue after counter reset.
            self.ui_failures = 0
            return

        # Escalation: restart process after repeated failures.
        LOGGER.error("Escalating recovery: restarting process '%s'", self.process_name)
        restart_process(self.process_name)
        self.ui_failures = 0
        self.recovery_attempts = 0
