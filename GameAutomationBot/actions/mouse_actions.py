"""Human-like mouse automation functions.

This module wraps PyAutoGUI calls with randomization to emulate natural behavior:
- click offsets
- movement durations
- micro-adjustments
- random post-action delays
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

# Global PyAutoGUI safety and pacing configuration.
pyautogui.FAILSAFE = FAILSAFE_ENABLED
pyautogui.PAUSE = PYAUTOGUI_PAUSE


def _apply_offset(value: int) -> int:
    """Apply random pixel offset around a target coordinate."""
    return value + random.randint(-MOUSE_OFFSET_PIXELS, MOUSE_OFFSET_PIXELS)


def human_move(x: int, y: int) -> None:
    """Move cursor to position with randomized duration and micro-jitter."""
    # Randomized move duration reduces robotic movement patterns.
    duration = random.uniform(MOUSE_MIN_DURATION, MOUSE_MAX_DURATION)
    pyautogui.moveTo(_apply_offset(x), _apply_offset(y), duration=duration)

    # Subtle pre-click movement helps mimic natural hand adjustments.
    pyautogui.moveRel(random.randint(-2, 2), random.randint(-2, 2), duration=0.02)


def human_click(x: int, y: int, button: str = "left") -> None:
    """Perform a humanized click at target coordinates."""
    human_move(x, y)
    pyautogui.click(button=button)

    # Random delay helps avoid repetitive cadence patterns.
    time.sleep(random.uniform(ACTION_DELAY_MIN, ACTION_DELAY_MAX))
