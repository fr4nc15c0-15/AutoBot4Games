"""Endfield exploration and resource gathering logic.

Implements a sample exploration cycle:
- detect resource node templates
- navigate map when no node found
- collect resource when node is found
"""

from __future__ import annotations

from actions.keyboard_actions import hold_key, press_key
from config.paths import RESOURCES_DIR
from core.bot_engine import BotEngine
from utils.logger import get_logger
from vision.image_detection import find_and_click

LOGGER = get_logger(__name__)


def run_exploration(engine: BotEngine) -> None:
    """Execute resource gathering loop for Endfield."""
    LOGGER.info("Starting Endfield exploration module")
    node_template = RESOURCES_DIR / "resource_node.png"

    for _ in range(8):
        found = find_and_click(node_template, confidence=0.76, timeout=1.5, retries=2)
        if found:
            # Interact key to gather resource after selecting node.
            press_key("f")
            engine.reset_ui_failures()
        else:
            engine.register_ui_failure("Resource node not found")
            # Move character forward to discover new nodes.
            hold_key("w", 0.75)
