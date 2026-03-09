"""Screen capture helpers built on PyAutoGUI and Pillow.

This module provides reusable screenshot functionality for OCR and CV tasks.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pyautogui
from PIL import Image


def capture(region: tuple[int, int, int, int] | None = None) -> Image.Image:
    """Capture a screen image.

    Args:
        region: Optional screen region tuple (left, top, width, height).
    """
    return pyautogui.screenshot(region=region)


def capture_np(region: tuple[int, int, int, int] | None = None) -> np.ndarray:
    """Capture a screen image and return it as a NumPy array in RGB format."""
    image: Image.Image = capture(region)
    return np.array(image)
