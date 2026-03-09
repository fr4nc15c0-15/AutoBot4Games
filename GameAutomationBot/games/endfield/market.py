"""Endfield market automation logic.

Handles item detection, OCR price reading, profit calculation, and trade actions.
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from ocr.price_reader import read_buy_price, read_sell_price
from vision.ui_detector import UIDetector
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def run_market() -> None:
    """Scan market prices and execute buy/sell when profitable."""
    LOGGER.info("Starting Endfield market automation")
    ui = UIDetector()
    buy = read_buy_price()
    sell = read_sell_price()

    if buy is None or sell is None:
        LOGGER.warning("Unable to read market prices")
        return

    profit = sell - buy
    LOGGER.info("Market profit estimate: %s", profit)
    if profit > 0:
        buy_btn = ui.detect_button("BUY")
        sell_btn = ui.detect_button("SELL")
        if buy_btn:
            human_click(*buy_btn)
        if sell_btn:
            human_click(*sell_btn)
