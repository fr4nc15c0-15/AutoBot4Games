"""Main orchestrator for GameAutomationBot.

This module coordinates sequential execution of supported game bots,
handles cleanup between runs, and provides a single entry point.
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
    """Run all configured game bots in sequence with cleanup between runs."""
    game_runs = [
        ("Arknights Endfield", EndfieldBot()),
        ("Solo Leveling Arise", SoloLevelingBot()),
        ("7DS Grand Cross", SevenDSBot()),
    ]

    for game_name, bot in game_runs:
        LOGGER.info("Starting bot for %s", game_name)
        try:
            bot.run()
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Unhandled error while running %s: %s", game_name, exc)
        finally:
            # Always attempt cleanup to keep the next run stable.
            close_game(bot.process_name)
            free_memory()
            LOGGER.info("Waiting %s seconds before next game", ORCHESTRATION_WAIT_SECONDS)
            time.sleep(ORCHESTRATION_WAIT_SECONDS)


if __name__ == "__main__":
    run_all_games()
