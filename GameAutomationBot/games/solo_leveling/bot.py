"""Solo Leveling Arise game orchestrator.

Coordinates gate and daily automation routines.
"""

from __future__ import annotations

from core.bot_engine import BotEngine
from games.solo_leveling.dailies import run_dailies
from games.solo_leveling.gates import run_gates


class SoloLevelingBot(BotEngine):
    """Solo Leveling automation orchestrator."""

    def __init__(self) -> None:
        super().__init__(process_name="solo_leveling")

    def run(self) -> None:
        """Execute Solo Leveling routines."""
        self.start_services()
        try:
            run_gates()
            run_dailies()
        finally:
            self.stop_services()
