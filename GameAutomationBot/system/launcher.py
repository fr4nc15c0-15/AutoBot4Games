"""Game launcher helpers for starting game executables.

This module abstracts game process startup and logging.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from utils.logger import get_logger

LOGGER = get_logger(__name__)


def launch_game(path: str | Path) -> subprocess.Popen | None:
    """Launch a game executable and return process handle if successful."""
    try:
        process = subprocess.Popen([str(path)], shell=False)
        LOGGER.info("Launched game: %s", path)
        return process
    except Exception as exc:  # noqa: BLE001
        LOGGER.exception("Failed to launch game at %s: %s", path, exc)
        return None
