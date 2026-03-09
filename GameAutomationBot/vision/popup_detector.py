"""Universal anti-popup detector running in a background thread.

It scans known popup templates and automatically closes dialogs.
"""

from __future__ import annotations

import threading
import time

from actions.mouse_actions import human_click
from config.paths import POPUPS_DIR
from config.settings import POPUP_SCAN_INTERVAL
from vision.template_matching import find_center
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class PopupDetector(threading.Thread):
    """Background popup scanner that closes common disruptive dialogs."""

    def __init__(self, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.stop_event = stop_event
        self.popup_templates = [
            POPUPS_DIR / "confirm.png",
            POPUPS_DIR / "reward_close.png",
            POPUPS_DIR / "connection_warning.png",
            POPUPS_DIR / "error_ok.png",
        ]

    def run(self) -> None:
        """Continuously detect and close popups while bot is active."""
        LOGGER.info("Popup detector started")
        while not self.stop_event.is_set():
            for template in self.popup_templates:
                if not template.exists():
                    continue
                center = find_center(template, confidence=0.8, timeout=1.0, retries=1)
                if center:
                    LOGGER.info("Popup detected via %s, closing", template.name)
                    human_click(*center)
                    time.sleep(0.2)
            time.sleep(POPUP_SCAN_INTERVAL)
        LOGGER.info("Popup detector stopped")
