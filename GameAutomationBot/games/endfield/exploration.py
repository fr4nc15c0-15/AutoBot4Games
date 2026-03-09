"""Endfield exploration logic.

Automates resource gathering by locating resource nodes and collecting them.
"""

from __future__ import annotations

from actions.keyboard_actions import hold_key, press_key
from vision.image_detection import find_and_click
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def run_exploration() -> None:
    """Perform exploration and resource gathering cycle."""
    LOGGER.info("Starting Endfield exploration")
    for _ in range(5):
        if find_and_click("assets/resources/node.png", confidence=0.78, timeout=2.0):
            press_key("f")  # Typical interaction key for collecting nodes.
        else:
            hold_key("w", 0.8)  # Move forward to discover new nodes.
