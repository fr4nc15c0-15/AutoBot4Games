"""7DS Grand Cross game orchestrator.

Coordinates farming and dailies under shared bot engine services.
"""

from __future__ import annotations

from core.bot_engine import BotEngine
from games.seven_ds.dailies import run_dailies
from games.seven_ds.farming import run_farming


class SevenDSBot(BotEngine):
    """7DS Grand Cross automation orchestrator."""

    def __init__(self) -> None:
        super().__init__(process_name="seven_ds")

    def run(self) -> None:
        """Execute configured 7DS automation routines."""
        self.start_services()
        try:
            run_farming()
            run_dailies()
        finally:
            self.stop_services()
