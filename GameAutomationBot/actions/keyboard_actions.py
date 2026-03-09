"""Keyboard automation utilities.

Provides reusable key press and hold wrappers with optional randomized delays.
"""

from __future__ import annotations

import random
import time

import pyautogui

from config.settings import ACTION_DELAY_MAX, ACTION_DELAY_MIN


def press_key(key: str) -> None:
    """Press and release one key with randomized cooldown delay."""
    pyautogui.press(key)
    time.sleep(random.uniform(ACTION_DELAY_MIN, ACTION_DELAY_MAX))


def hold_key(key: str, hold_seconds: float) -> None:
    """Hold a key for a specified duration and release it."""
    pyautogui.keyDown(key)
    time.sleep(hold_seconds)
    pyautogui.keyUp(key)
