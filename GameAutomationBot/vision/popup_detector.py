"""Background anti-popup detector.

This thread continuously scans for known popup templates and closes them
without interrupting primary gameplay tasks.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

from actions.mouse_actions import human_click
from config.paths import POPUPS_DIR
from config.settings import POPUP_SCAN_INTERVAL
from utils.logger import get_logger
from vision.template_matching import find_center

LOGGER = get_logger(__name__)


class PopupDetector(threading.Thread):
    """Thread that auto-closes common dialogs and warning popups."""

    def __init__(self, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.stop_event = stop_event
        self.popup_templates: list[Path] = [
            POPUPS_DIR / "confirmation.png",
            POPUPS_DIR / "reward_close.png",
            POPUPS_DIR / "connection_warning.png",
            POPUPS_DIR / "error_ok.png",
        ]

    def run(self) -> None:
        """Main popup scanning loop."""
        LOGGER.info("Popup detector started")
        while not self.stop_event.is_set():
            for template in self.popup_templates:
                if not template.exists():
                    # Skip missing templates so deployment can start with partial assets.
                    continue

                center = find_center(template, confidence=0.80, timeout=1.2, retries=1)
                if center:
                    LOGGER.info("Closing popup via template %s", template.name)
                    human_click(*center)
                    time.sleep(0.15)

            time.sleep(POPUP_SCAN_INTERVAL)
        LOGGER.info("Popup detector stopped")
