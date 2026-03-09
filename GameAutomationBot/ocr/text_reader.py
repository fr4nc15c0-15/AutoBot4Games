"""OCR text extraction utilities with preprocessing pipeline.

This module turns screen regions into cleaner OCR input for better accuracy.
"""

from __future__ import annotations

import cv2
import numpy as np
import pytesseract

from config.settings import OCR_LANG, OCR_PSM_MODE
from vision.screen_capture import capture_np


def _preprocess_for_ocr(image_rgb: np.ndarray) -> np.ndarray:
    """Apply grayscale, denoise, threshold, and contrast enhancements."""
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    denoised = cv2.medianBlur(gray, 3)
    equalized = cv2.equalizeHist(denoised)
    _, thresh = cv2.threshold(equalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def read_text(region: tuple[int, int, int, int]) -> str:
    """Read free-form text from a specific screen region."""
    image = capture_np(region)
    processed = _preprocess_for_ocr(image)
    config = f"--oem 3 --psm {OCR_PSM_MODE}"
    return pytesseract.image_to_string(processed, lang=OCR_LANG, config=config).strip()


def read_number(region: tuple[int, int, int, int]) -> int | None:
    """Read numeric content from region and return integer if parseable."""
    image = capture_np(region)
    processed = _preprocess_for_ocr(image)
    config = "--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789"
    value = pytesseract.image_to_string(processed, lang=OCR_LANG, config=config).strip()
    try:
        return int(value)
    except ValueError:
        return None
