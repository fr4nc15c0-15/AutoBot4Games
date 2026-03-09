"""Solo Leveling gate automation logic.

Automates entering and clearing available gates.
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from vision.ui_detector import UIDetector


def run_gates() -> None:
    """Enter gate interface and start a run."""
    ui = UIDetector()
    for label in ["GATE", "START", "CONFIRM"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
