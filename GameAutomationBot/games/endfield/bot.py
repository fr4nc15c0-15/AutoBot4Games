"""Endfield game orchestrator.

This module wires all Endfield sub-modules into one execution flow.
"""

from __future__ import annotations

from core.bot_engine import BotEngine
from games.endfield.combat import run_combat
from games.endfield.dailies import run_dailies
from games.endfield.exploration import run_exploration
from games.endfield.market import run_market
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class EndfieldBot(BotEngine):
    """Arknights Endfield automation orchestrator."""

    def __init__(self) -> None:
        super().__init__(process_name="endfield")

    def run(self) -> None:
        """Run all Endfield routines in required order."""
        self.start_services()
        try:
            run_exploration()
            run_market()
            run_dailies()
            run_combat()
        finally:
            self.stop_services()
            LOGGER.info("Endfield run complete")
