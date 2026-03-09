"""Optimized OpenCV template matching utilities.

Implements `find_image` and `find_center` with support for:
- grayscale matching
- adjustable confidence
- region-restricted search
- timeout
- retry loop
"""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np

from config.settings import (
    DEFAULT_RETRY_COUNT,
    DEFAULT_RETRY_DELAY,
    DEFAULT_TEMPLATE_CONFIDENCE,
    DEFAULT_TIMEOUT_SECONDS,
)
from vision.screen_capture import capture_np


def _prepare_frame(frame_rgb: np.ndarray, grayscale: bool) -> np.ndarray:
    """Convert captured RGB frame into OpenCV format needed for matching."""
    if grayscale:
        return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
    return cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)


def find_image(
    template_path: str | Path,
    confidence: float = DEFAULT_TEMPLATE_CONFIDENCE,
    grayscale: bool = True,
    region: tuple[int, int, int, int] | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRY_COUNT,
) -> tuple[int, int, int, int] | None:
    """Find template on screen and return absolute bounding rectangle.

    Args:
        template_path: Path to the template image.
        confidence: Required match confidence (0.0 - 1.0).
        grayscale: Whether to run grayscale matching.
        region: Optional search region `(left, top, width, height)`.
        timeout: Maximum search time in seconds.
        retries: Number of polling attempts.
    """
    # Load template once to avoid repeated file I/O in retry loop.
    template = cv2.imread(
        str(template_path),
        cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR,
    )
    if template is None:
        return None

    start_time = time.time()
    attempts = 0

    while attempts < max(retries, 1):
        # Stop if timeout budget was consumed.
        if time.time() - start_time > timeout:
            break

        frame = _prepare_frame(capture_np(region), grayscale)

        # Run normalized correlation coefficient matching.
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_value, _, max_location = cv2.minMaxLoc(result)

        if max_value >= confidence:
            x, y = max_location
            height, width = template.shape[:2]

            # Convert region-relative coordinates into absolute screen coordinates.
            if region:
                x += region[0]
                y += region[1]

            return (x, y, width, height)

        attempts += 1
        time.sleep(DEFAULT_RETRY_DELAY)

    return None


def find_center(*args, **kwargs) -> tuple[int, int] | None:
    """Find template and return center coordinate `(x, y)` if matched."""
    rect = find_image(*args, **kwargs)
    if rect is None:
        return None

    x, y, width, height = rect
    return (x + width // 2, y + height // 2)
