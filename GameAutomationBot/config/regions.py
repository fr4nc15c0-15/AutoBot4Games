"""Named screen regions used by OCR and computer vision.

Regions use the tuple format: (left, top, width, height).
"""

from __future__ import annotations

REGIONS = {
    "full_screen": (0, 0, 1920, 1080),
    "top_bar": (0, 0, 1920, 120),
    "center_panel": (480, 240, 960, 600),
    "right_panel": (1440, 120, 480, 900),
    "bottom_bar": (0, 900, 1920, 180),
    "market_prices": (1200, 250, 500, 450),
}
