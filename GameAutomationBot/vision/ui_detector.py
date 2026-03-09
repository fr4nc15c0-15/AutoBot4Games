"""Universal UI detector implementation.

Detection order is intentionally strict:
1) Template matching
2) OCR text recognition
3) Region fallback heuristic
"""

from __future__ import annotations

from pathlib import Path

from config.paths import BUTTONS_DIR
from config.regions import REGIONS
from ocr.text_reader import read_text
from vision.template_matching import find_center


class UIDetector:
    """Generic detector for buttons and UI text across supported games."""

    def detect_button(
        self,
        label: str,
        search_region: tuple[int, int, int, int] | None = None,
    ) -> tuple[int, int] | None:
        """Detect button by label using template, OCR, then fallback strategy.

        Args:
            label: Button text label (e.g., "PLAY").
            search_region: Optional region override for OCR + template scan.
        """
        normalized = label.lower().replace(" ", "_")
        template_path = BUTTONS_DIR / f"{normalized}.png"

        # 1) Template first for highest precision when assets are available.
        if template_path.exists():
            point = find_center(template_path, region=search_region)
            if point:
                return point

        # 2) OCR text scan to find textual presence in likely panel region.
        ocr_region = search_region or REGIONS["center_panel"]
        detected_text = read_text(ocr_region)
        if label.lower() in detected_text.lower():
            x, y, w, h = ocr_region
            # Approximate panel center when OCR confirms presence.
            return (x + w // 2, y + h // 2)

        # 3) Region fallback heuristic for common confirm/start actions.
        if label.upper() in {"OK", "CONFIRM", "PLAY", "START"}:
            x, y, w, h = REGIONS["bottom_bar"]
            return (x + w // 2, y + h // 2)

        return None
