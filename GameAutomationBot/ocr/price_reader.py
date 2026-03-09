"""Price-reading convenience functions for market automation modules."""

from __future__ import annotations

from config.regions import REGIONS
from ocr.text_reader import read_number


def read_buy_price() -> int | None:
    """Read market buy price from configured region."""
    return read_number(REGIONS["market_buy_price"])


def read_sell_price() -> int | None:
    """Read market sell price from configured region."""
    return read_number(REGIONS["market_sell_price"])
