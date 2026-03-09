"""Game launcher utility functions.

Responsible for starting executables in a controlled and logged manner.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from utils.logger import get_logger

LOGGER = get_logger(__name__)


def launch_game(path: str | Path) -> subprocess.Popen[bytes] | None:
    """Launch a game executable and return process handle when successful."""
    executable = Path(path)
    if not executable.exists():
        LOGGER.error("Executable not found: %s", executable)
        return None

    try:
        process = subprocess.Popen([str(executable)], shell=False)
        LOGGER.info("Launched game executable: %s", executable)
        return process
    except Exception as exc:  # noqa: BLE001
        LOGGER.exception("Failed to launch game '%s': %s", executable, exc)
        return None
