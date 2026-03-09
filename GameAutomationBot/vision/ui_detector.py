"""Universal UI detector combining template matching and OCR.

Detection order:
1) template matching
2) OCR text lookup
3) fallback search region heuristics
"""

from __future__ import annotations

from pathlib import Path

from config.paths import BUTTONS_DIR
from config.regions import REGIONS
from ocr.text_reader import read_text
from vision.template_matching import find_center


class UIDetector:
    """Unified API for locating buttons and UI elements across games."""

    def detect_button(self, label: str) -> tuple[int, int] | None:
        """Detect button center by label using template, OCR, then fallback."""
        template = BUTTONS_DIR / f"{label.lower().replace(' ', '_')}.png"

        # 1) Template matching for highest precision when assets exist.
        if template.exists():
            center = find_center(template)
            if center:
                return center

        # 2) OCR lookup in known central panel where buttons typically exist.
        panel = REGIONS["center_panel"]
        text = read_text(panel)
        if label.lower() in text.lower():
            # Approximate center of panel as fallback click target for OCR hit.
            x, y, w, h = panel
            return (x + w // 2, y + h // 2)

        # 3) Fallback heuristic: use bottom bar center for common confirm actions.
        if label.upper() in {"OK", "CONFIRM", "PLAY", "START"}:
            x, y, w, h = REGIONS["bottom_bar"]
            return (x + w // 2, y + h // 2)
        return None
