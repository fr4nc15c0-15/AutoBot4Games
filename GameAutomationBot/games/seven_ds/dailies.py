"""7DS dailies automation module."""

from __future__ import annotations

from actions.mouse_actions import human_click
from core.bot_engine import BotEngine
from utils.logger import get_logger
from vision.ui_detector import UIDetector

LOGGER = get_logger(__name__)


def run_dailies(engine: BotEngine) -> None:
    """Run daily check-in and reward claim flow."""
    LOGGER.info("Starting 7DS dailies module")
    ui = UIDetector()

    for label in ["DAILIES", "CLAIM", "CONFIRM"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
            engine.reset_ui_failures()
        else:
            engine.register_ui_failure(f"Missing dailies button: {label}")
