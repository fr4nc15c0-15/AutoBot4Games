"""7DS farming automation module."""

from __future__ import annotations

from actions.mouse_actions import human_click
from core.bot_engine import BotEngine
from utils.logger import get_logger
from vision.ui_detector import UIDetector

LOGGER = get_logger(__name__)


def run_farming(engine: BotEngine) -> None:
    """Execute battle-repeat style farming setup flow."""
    LOGGER.info("Starting 7DS farming module")
    ui = UIDetector()

    for label in ["BATTLE", "REPEAT", "START"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
            engine.reset_ui_failures()
        else:
            engine.register_ui_failure(f"Missing farming button: {label}")
