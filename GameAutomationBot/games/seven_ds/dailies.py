"""7DS daily missions automation.

Performs daily check-in and reward claim click paths.
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from vision.ui_detector import UIDetector


def run_dailies() -> None:
    """Run daily reward collection sequence."""
    ui = UIDetector()
    for label in ["DAILIES", "CLAIM", "CONFIRM"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
