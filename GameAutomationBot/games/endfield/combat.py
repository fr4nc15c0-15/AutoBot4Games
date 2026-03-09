"""Endfield combat farming automation.

Executes repeated combat starts, skill keys, and completion confirmations.
"""

from __future__ import annotations

from actions.keyboard_actions import press_key
from vision.image_detection import find_and_click
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def run_combat() -> None:
    """Run a basic combat farming cycle."""
    LOGGER.info("Running Endfield combat farming")
    find_and_click("assets/buttons/start_combat.png", confidence=0.8, timeout=3)
    for key in ["1", "2", "3", "space"]:
        press_key(key)
    find_and_click("assets/buttons/confirm.png", confidence=0.75, timeout=2)
