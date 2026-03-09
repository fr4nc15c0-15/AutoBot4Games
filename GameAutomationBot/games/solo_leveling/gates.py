"""Solo Leveling gates automation module."""

from __future__ import annotations

from actions.mouse_actions import human_click
from core.bot_engine import BotEngine
from utils.logger import get_logger
from vision.ui_detector import UIDetector

LOGGER = get_logger(__name__)


def run_gates(engine: BotEngine) -> None:
    """Navigate to gates and start a run."""
    LOGGER.info("Starting Solo Leveling gates module")
    ui = UIDetector()

    for label in ["GATE", "START", "CONFIRM"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
            engine.reset_ui_failures()
        else:
            engine.register_ui_failure(f"Missing gate flow button: {label}")
