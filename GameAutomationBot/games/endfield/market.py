"""Endfield market/trading automation logic.

Responsibilities:
- detect item/action buttons
- read buy/sell prices
- calculate profit
- perform buy/sell actions when profitable
"""

from __future__ import annotations

from actions.mouse_actions import human_click
from core.bot_engine import BotEngine
from ocr.price_reader import read_buy_price, read_sell_price
from utils.logger import get_logger
from vision.ui_detector import UIDetector

LOGGER = get_logger(__name__)


def run_market(engine: BotEngine) -> None:
    """Execute basic market trade strategy."""
    LOGGER.info("Starting Endfield market module")
    ui = UIDetector()

    buy_price = read_buy_price()
    sell_price = read_sell_price()

    if buy_price is None or sell_price is None:
        engine.register_ui_failure("Could not OCR buy/sell prices")
        return

    profit = sell_price - buy_price
    LOGGER.info("Market prices | buy=%s sell=%s profit=%s", buy_price, sell_price, profit)

    if profit <= 0:
        LOGGER.info("Skipping market trade because profit is non-positive")
        engine.reset_ui_failures()
        return

    buy_button = ui.detect_button("BUY")
    sell_button = ui.detect_button("SELL")

    if not buy_button or not sell_button:
        engine.register_ui_failure("Buy/Sell buttons not detected")
        return

    # Execute buy then sell in sequence when profitable.
    human_click(*buy_button)
    human_click(*sell_button)
    engine.reset_ui_failures()
