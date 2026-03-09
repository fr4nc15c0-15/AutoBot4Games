"""Human-like mouse automation utilities.

This module provides randomized movement, offset, and delay logic for safer input.
"""

from __future__ import annotations

import random
import time

import pyautogui

from config.settings import (
    ACTION_DELAY_MAX,
    ACTION_DELAY_MIN,
    FAILSAFE_ENABLED,
    MOUSE_MAX_DURATION,
    MOUSE_MIN_DURATION,
    MOUSE_OFFSET_PIXELS,
    PYAUTOGUI_PAUSE,
)

pyautogui.FAILSAFE = FAILSAFE_ENABLED
pyautogui.PAUSE = PYAUTOGUI_PAUSE


def _jitter(point: int) -> int:
    """Apply a small random pixel offset to mimic human movement variance."""
    return point + random.randint(-MOUSE_OFFSET_PIXELS, MOUSE_OFFSET_PIXELS)


def human_move(x: int, y: int) -> None:
    """Move cursor with randomized duration and pre-click micro-adjustment."""
    duration = random.uniform(MOUSE_MIN_DURATION, MOUSE_MAX_DURATION)
    pyautogui.moveTo(_jitter(x), _jitter(y), duration=duration)
    # Small micro movement before click for human-like behavior.
    pyautogui.moveRel(random.randint(-2, 2), random.randint(-2, 2), duration=0.02)


def human_click(x: int, y: int, button: str = "left") -> None:
    """Perform a human-like click with random movement and delay."""
    human_move(x, y)
    pyautogui.click(button=button)
    time.sleep(random.uniform(ACTION_DELAY_MIN, ACTION_DELAY_MAX))
