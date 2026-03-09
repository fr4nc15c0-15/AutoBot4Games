"""7DS farming automation routines.

Executes repeat-battle style interactions for farming resources.
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from vision.ui_detector import UIDetector


def run_farming() -> None:
    """Run farming loop entry sequence."""
    ui = UIDetector()
    for label in ["BATTLE", "REPEAT", "START"]:
        point = ui.detect_button(label)
        if point:
            human_click(*point)
