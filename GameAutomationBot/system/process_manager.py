"""Process management and recovery utilities.

This module provides process checks, close/kill helpers, and restart workflows.
"""

from __future__ import annotations

import psutil

from config.paths import GAME_EXECUTABLES
from system.launcher import launch_game
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def is_process_running(process_name: str) -> bool:
    """Return True when a process with matching name is currently active."""
    for proc in psutil.process_iter(attrs=["name"]):
        if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
            return True
    return False


def close_game(process_name: str) -> None:
    """Gracefully terminate matching game process names."""
    for proc in psutil.process_iter(attrs=["name"]):
        if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
            LOGGER.info("Closing process %s (pid=%s)", proc.info["name"], proc.pid)
            proc.terminate()


def kill_if_not_responding(process_name: str) -> bool:
    """Kill suspended/zombie/unresponsive game process and return True if killed."""
    for proc in psutil.process_iter(attrs=["name", "status"]):
        if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
            if proc.info.get("status") in {psutil.STATUS_ZOMBIE, psutil.STATUS_STOPPED}:
                proc.kill()
                return True
    return False


def restart_process(process_name: str) -> None:
    """Restart a process using configured executable mapping when available."""
    close_game(process_name)
    executable = GAME_EXECUTABLES.get(process_name)
    if executable:
        launch_game(executable)
    else:
        LOGGER.error("No executable configured for process alias: %s", process_name)
