"""Screen capture helpers.

This module captures screenshots using PyAutoGUI and returns either Pillow image
objects or NumPy arrays for OpenCV/OCR processing.
"""

from __future__ import annotations

import numpy as np
import pyautogui
from PIL import Image


def capture(region: tuple[int, int, int, int] | None = None) -> Image.Image:
    """Capture a screenshot of the whole screen or a specific region."""
    return pyautogui.screenshot(region=region)


def capture_np(region: tuple[int, int, int, int] | None = None) -> np.ndarray:
    """Capture screenshot and return RGB NumPy array for downstream CV/OCR."""
    image = capture(region)
    return np.array(image)
