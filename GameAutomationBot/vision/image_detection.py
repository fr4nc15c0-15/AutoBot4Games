"""High-level image detection helpers.

Includes convenience API to detect an image and click it in one step.
"""

from __future__ import annotations

from pathlib import Path

from actions.mouse_actions import human_click
from vision.template_matching import find_center


def find_and_click(template_path: str | Path, **kwargs) -> bool:
    """Locate image center and click it.

    Returns:
        True when image was found and clicked, otherwise False.
    """
    center = find_center(template_path, **kwargs)
    if center is None:
        return False

    human_click(*center)
    return True
