"""Named screen regions used for OCR and targeted detection.

Each region is expressed as `(left, top, width, height)` in screen pixels.
These defaults target a 1920x1080 profile and can be tuned per user setup.
"""

from __future__ import annotations

REGIONS = {
    # Full-screen capture fallback.
    "full_screen": (0, 0, 1920, 1080),
    # Standard UI areas.
    "top_bar": (0, 0, 1920, 130),
    "center_panel": (420, 200, 1080, 640),
    "right_panel": (1450, 120, 470, 900),
    "bottom_bar": (0, 900, 1920, 180),
    # Market-oriented sample regions.
    "market_buy_price": (1250, 315, 220, 70),
    "market_sell_price": (1500, 315, 220, 70),
}
