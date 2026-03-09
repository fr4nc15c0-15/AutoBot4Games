"""Endfield daily mission automation.

Runs common daily mission interactions with robust UI detection.
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from vision.ui_detector import UIDetector
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def run_dailies() -> None:
    """Complete configured daily mission actions."""
    LOGGER.info("Running Endfield dailies")
    ui = UIDetector()
    for label in ["MISSIONS", "CLAIM", "CONFIRM"]:
        button = ui.detect_button(label)
        if button:
            human_click(*button)
