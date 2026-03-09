"""Endfield daily mission automation module."""

from __future__ import annotations

from actions.mouse_actions import human_click
from core.bot_engine import BotEngine
from utils.logger import get_logger
from vision.ui_detector import UIDetector

LOGGER = get_logger(__name__)


def run_dailies(engine: BotEngine) -> None:
    """Run daily mission collection flow for Endfield."""
    LOGGER.info("Starting Endfield dailies module")
    ui = UIDetector()

    for label in ["MISSIONS", "CLAIM", "CONFIRM"]:
        button = ui.detect_button(label)
        if button:
            human_click(*button)
            engine.reset_ui_failures()
        else:
            engine.register_ui_failure(f"Missing daily button: {label}")
