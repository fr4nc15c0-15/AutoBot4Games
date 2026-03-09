"""Endfield combat farming module."""

from __future__ import annotations

from actions.keyboard_actions import press_key
from config.paths import BUTTONS_DIR
from core.bot_engine import BotEngine
from utils.logger import get_logger
from vision.image_detection import find_and_click

LOGGER = get_logger(__name__)


def run_combat(engine: BotEngine) -> None:
    """Run sample combat-farming sequence."""
    LOGGER.info("Starting Endfield combat module")

    start_clicked = find_and_click(BUTTONS_DIR / "start_combat.png", confidence=0.80, timeout=2.5, retries=2)
    if not start_clicked:
        engine.register_ui_failure("Start combat button not found")
        return

    # Example skill cycle for automated combat farming.
    for key in ["1", "2", "3", "space"]:
        press_key(key)

    # Confirm rewards/complete screens if visible.
    find_and_click(BUTTONS_DIR / "confirm.png", confidence=0.78, timeout=1.8, retries=1)
    engine.reset_ui_failures()
