"""Filesystem and executable path configuration.

All paths used by the framework are defined here to avoid hard-coded literals
across modules.
"""

from __future__ import annotations

from pathlib import Path

# Root folder for the generated project.
BASE_DIR = Path(__file__).resolve().parents[1]

# Asset and log roots.
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"

# Asset categories.
BUTTONS_DIR = ASSETS_DIR / "buttons"
ITEMS_DIR = ASSETS_DIR / "items"
POPUPS_DIR = ASSETS_DIR / "popups"
RESOURCES_DIR = ASSETS_DIR / "resources"

# Executable map by bot process alias (same alias used by bot classes).
GAME_EXECUTABLES = {
    "endfield": Path(r"C:/Games/Endfield/Endfield.exe"),
    "solo_leveling": Path(r"C:/Games/SoloLevelingArise/SoloLevelingArise.exe"),
    "seven_ds": Path(r"C:/Games/SevenDS/SevenDS.exe"),
}
