"""OCR text and numeric extraction utilities.

Provides preprocessing pipeline:
- grayscale conversion
- noise removal
- contrast enhancement
- thresholding
"""

from __future__ import annotations

import cv2
import numpy as np
import pytesseract

from config.settings import OCR_LANG, OCR_PSM_MODE
from vision.screen_capture import capture_np


def _preprocess_for_ocr(frame_rgb: np.ndarray) -> np.ndarray:
    """Apply OCR-friendly image preprocessing pipeline."""
    # Convert to grayscale to reduce channel noise.
    gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

    # Median blur helps suppress isolated pixel noise.
    denoised = cv2.medianBlur(gray, 3)

    # Histogram equalization improves contrast in low-light UIs.
    enhanced = cv2.equalizeHist(denoised)

    # OTSU thresholding binarizes text/background separation.
    _, thresholded = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresholded


def read_text(region: tuple[int, int, int, int]) -> str:
    """Read general text from a region.

    Args:
        region: `(left, top, width, height)` target region.
    """
    frame = capture_np(region)
    processed = _preprocess_for_ocr(frame)
    config = f"--oem 3 --psm {OCR_PSM_MODE}"
    return pytesseract.image_to_string(processed, lang=OCR_LANG, config=config).strip()


def read_number(region: tuple[int, int, int, int]) -> int | None:
    """Read numeric value from a region and convert to `int` when possible."""
    frame = capture_np(region)
    processed = _preprocess_for_ocr(frame)

    # Restrict OCR character set to digits for better numeric accuracy.
    config = "--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789"
    raw = pytesseract.image_to_string(processed, lang=OCR_LANG, config=config).strip()

    try:
        return int(raw)
    except ValueError:
        return None
