"""Keyboard automation helpers with randomized delays.

This module wraps pyautogui keyboard primitives for reusable game actions.
"""

from __future__ import annotations

import random
import time

import pyautogui

from config.settings import ACTION_DELAY_MAX, ACTION_DELAY_MIN


def press_key(key: str) -> None:
    """Press and release a single key with a randomized follow-up delay."""
    pyautogui.press(key)
    time.sleep(random.uniform(ACTION_DELAY_MIN, ACTION_DELAY_MAX))


def hold_key(key: str, seconds: float) -> None:
    """Hold a key for a fixed duration."""
    pyautogui.keyDown(key)
    time.sleep(seconds)
    pyautogui.keyUp(key)
