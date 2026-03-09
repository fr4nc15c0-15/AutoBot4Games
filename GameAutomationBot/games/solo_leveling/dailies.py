"""Solo Leveling daily mission automation.

Performs claim and mission navigation actions.
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from vision.ui_detector import UIDetector


def run_dailies() -> None:
    """Run daily mission claim sequence."""
    ui = UIDetector()
    for label in ["MISSIONS", "CLAIM", "OK"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
