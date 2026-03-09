"""Price-reading helper module for market automation logic.

This module builds on OCR utilities to parse buy/sell prices from known regions.
"""

from __future__ import annotations

from config.regions import REGIONS
from ocr.text_reader import read_number


def read_buy_price() -> int | None:
    """Read buy price from market panel region."""
    return read_number(REGIONS["market_prices"])


def read_sell_price() -> int | None:
    """Read sell price from market panel region.

    In a production profile, this can point to a dedicated sell-price subregion.
    """
    return read_number(REGIONS["market_prices"])
