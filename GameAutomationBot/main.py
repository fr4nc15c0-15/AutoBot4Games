"""Application entry point for the GameAutomationBot master orchestrator.

This module runs each supported game bot sequentially. It also performs
inter-run cleanup (process close + memory cleanup + wait period) to reduce
cross-game interference and keep long sessions stable.
"""

from __future__ import annotations

import time

from config.settings import ORCHESTRATION_WAIT_SECONDS
from games.endfield.bot import EndfieldBot
from games.seven_ds.bot import SevenDSBot
from games.solo_leveling.bot import SoloLevelingBot
from system.memory_manager import free_memory
from system.process_manager import close_game
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def run_all_games() -> None:
    """Run all configured game bots in the required sequence.

    Order:
    1) Arknights Endfield
    2) Solo Leveling Arise
    3) 7DS Grand Cross
    """
    # Instantiate bot objects once for clear control flow and predictable teardown.
    game_runs = [
        ("Arknights Endfield", EndfieldBot()),
        ("Solo Leveling Arise", SoloLevelingBot()),
        ("7DS Grand Cross", SevenDSBot()),
    ]

    for game_name, bot in game_runs:
        LOGGER.info("Starting bot for %s", game_name)
        try:
            # Run game-specific workflow through its orchestrator.
            bot.run()
        except Exception as exc:  # noqa: BLE001 - top-level guard for uninterrupted orchestration.
            LOGGER.exception("Unhandled orchestration error for %s: %s", game_name, exc)
        finally:
            # Always clean up game process and memory before next game.
            close_game(bot.process_name)
            free_memory()
            LOGGER.info("Waiting %s seconds before next game", ORCHESTRATION_WAIT_SECONDS)
            time.sleep(ORCHESTRATION_WAIT_SECONDS)


if __name__ == "__main__":
    run_all_games()
