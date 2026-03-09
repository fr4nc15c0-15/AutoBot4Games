"""Process management utilities for game lifecycle control.

Includes:
- process existence checks
- graceful process shutdown
- unresponsive process kill
- restart by configured executable alias
"""

from __future__ import annotations

import psutil

from config.paths import GAME_EXECUTABLES
from system.launcher import launch_game
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def is_process_running(process_name: str) -> bool:
    """Check if a process containing `process_name` in its name is running."""
    for proc in psutil.process_iter(attrs=["name"]):
        name = proc.info.get("name")
        if name and process_name.lower() in name.lower():
            return True
    return False


def close_game(process_name: str) -> None:
    """Terminate all processes with names containing `process_name`."""
    for proc in psutil.process_iter(attrs=["name"]):
        name = proc.info.get("name")
        if name and process_name.lower() in name.lower():
            LOGGER.info("Terminating process %s (pid=%s)", name, proc.pid)
            try:
                proc.terminate()
            except psutil.Error as exc:
                LOGGER.warning("Failed to terminate %s (pid=%s): %s", name, proc.pid, exc)


def kill_if_not_responding(process_name: str) -> bool:
    """Kill non-healthy process states and return True if a kill occurred."""
    killed_any = False
    for proc in psutil.process_iter(attrs=["name", "status"]):
        name = proc.info.get("name")
        status = proc.info.get("status")
        if name and process_name.lower() in name.lower():
            if status in {psutil.STATUS_ZOMBIE, psutil.STATUS_STOPPED}:
                LOGGER.warning("Killing unhealthy process %s (pid=%s, status=%s)", name, proc.pid, status)
                try:
                    proc.kill()
                    killed_any = True
                except psutil.Error as exc:
                    LOGGER.warning("Failed to kill %s (pid=%s): %s", name, proc.pid, exc)
    return killed_any


def restart_process(process_name: str) -> None:
    """Restart a game process by alias from `GAME_EXECUTABLES`."""
    close_game(process_name)
    executable = GAME_EXECUTABLES.get(process_name)
    if not executable:
        LOGGER.error("No executable configured for process alias '%s'", process_name)
        return
    launch_game(executable)
