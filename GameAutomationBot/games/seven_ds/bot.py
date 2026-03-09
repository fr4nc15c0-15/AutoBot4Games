"""7DS bot orchestrator."""

from __future__ import annotations

from core.bot_engine import BotEngine
from games.seven_ds.dailies import run_dailies
from games.seven_ds.farming import run_farming
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class SevenDSBot(BotEngine):
    """Orchestrates 7DS farming and daily routines."""

    def __init__(self) -> None:
        super().__init__(process_name="seven_ds")

    def run(self) -> None:
        """Run 7DS modules under shared engine services."""
        self.start_services()
        try:
            run_farming(self)
            run_dailies(self)
        finally:
            self.stop_services()
            LOGGER.info("7DS run completed")
