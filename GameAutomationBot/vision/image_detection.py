"""High-level image detection wrappers for click workflows.

This module exposes find-and-click helpers to simplify game routines.
"""

from __future__ import annotations

from pathlib import Path

from actions.mouse_actions import human_click
from vision.template_matching import find_center


def find_and_click(template_path: str | Path, **kwargs) -> bool:
    """Locate template center and perform a human-like click."""
    center = find_center(template_path, **kwargs)
    if center is None:
        return False
    human_click(*center)
    return True
