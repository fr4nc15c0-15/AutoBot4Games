"""Fast OpenCV template matching utilities.

This module implements optimized template search with confidence, region support,
timeouts, and retries.
"""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np

from config.settings import DEFAULT_RETRY_COUNT, DEFAULT_RETRY_DELAY, DEFAULT_TEMPLATE_CONFIDENCE, DEFAULT_TIMEOUT_SECONDS
from vision.screen_capture import capture_np


def _prepare_image(image: np.ndarray, grayscale: bool) -> np.ndarray:
    """Convert an RGB screenshot to the required OpenCV color space."""
    if grayscale:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def find_image(
    template_path: str | Path,
    confidence: float = DEFAULT_TEMPLATE_CONFIDENCE,
    grayscale: bool = True,
    region: tuple[int, int, int, int] | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRY_COUNT,
) -> tuple[int, int, int, int] | None:
    """Find the best matching template on screen.

    Returns the bounding rectangle (x, y, w, h) in absolute screen coordinates.
    """
    template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
    if template is None:
        return None

    start = time.time()
    attempts = 0
    while attempts < retries and (time.time() - start) < timeout:
        screenshot = _prepare_image(capture_np(region), grayscale)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= confidence:
            x, y = max_loc
            h, w = template.shape[:2]
            if region:
                x += region[0]
                y += region[1]
            return (x, y, w, h)
        attempts += 1
        time.sleep(DEFAULT_RETRY_DELAY)
    return None


def find_center(*args, **kwargs) -> tuple[int, int] | None:
    """Find image and return center coordinates."""
    match = find_image(*args, **kwargs)
    if not match:
        return None
    x, y, w, h = match
    return (x + w // 2, y + h // 2)
