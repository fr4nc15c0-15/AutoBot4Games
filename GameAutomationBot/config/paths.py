"""Filesystem and executable path definitions.

This module centralizes paths for assets, logs, and game executables.
"""

from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"

BUTTONS_DIR = ASSETS_DIR / "buttons"
ITEMS_DIR = ASSETS_DIR / "items"
POPUPS_DIR = ASSETS_DIR / "popups"
RESOURCES_DIR = ASSETS_DIR / "resources"

GAME_EXECUTABLES = {
    "endfield": Path(r"C:/Games/Endfield/Endfield.exe"),
    "solo_leveling": Path(r"C:/Games/SoloLevelingArise/SLA.exe"),
    "seven_ds": Path(r"C:/Games/7DSGrandCross/7DS.exe"),
}
