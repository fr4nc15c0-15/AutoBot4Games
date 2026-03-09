"""Solo Leveling bot orchestrator."""

from __future__ import annotations

from core.bot_engine import BotEngine
from games.solo_leveling.dailies import run_dailies
from games.solo_leveling.gates import run_gates
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class SoloLevelingBot(BotEngine):
    """Orchestrates Solo Leveling automation routines."""

    def __init__(self) -> None:
        super().__init__(process_name="solo_leveling")

    def run(self) -> None:
        """Run gate and dailies modules."""
        self.start_services()
        try:
            run_gates(self)
            run_dailies(self)
        finally:
            self.stop_services()
            LOGGER.info("Solo Leveling run completed")
