"""Endfield bot orchestrator.

Coordinates exploration, market, dailies, and combat modules.
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
    """Game-specific orchestrator for Arknights Endfield."""

    def __init__(self) -> None:
        super().__init__(process_name="endfield")

    def run(self) -> None:
        """Run Endfield modules in required business order."""
        self.start_services()
        try:
            run_exploration(self)
            run_market(self)
            run_dailies(self)
            run_combat(self)
        finally:
            self.stop_services()
            LOGGER.info("Endfield run completed")
