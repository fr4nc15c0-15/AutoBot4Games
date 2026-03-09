"""Central settings for timing, retries, confidence, and behavior.

This module contains global bot constants used throughout the framework.
"""

from __future__ import annotations

# PyAutoGUI behavior and failsafe settings.
PYAUTOGUI_PAUSE = 0.05
FAILSAFE_ENABLED = True

# Detection defaults.
DEFAULT_TEMPLATE_CONFIDENCE = 0.85
DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_DELAY = 0.5

# OCR defaults.
OCR_PSM_MODE = 7
OCR_LANG = "eng"

# Human-like input settings.
MOUSE_OFFSET_PIXELS = 6
MOUSE_MIN_DURATION = 0.08
MOUSE_MAX_DURATION = 0.2
ACTION_DELAY_MIN = 0.05
ACTION_DELAY_MAX = 0.2

# Background services.
POPUP_SCAN_INTERVAL = 1.0
WATCHDOG_INTERVAL = 2.0
SCHEDULER_INTERVAL = 1.0
FREEZE_TIMEOUT_SECONDS = 45.0

# Recovery policy.
MAX_UI_FAILURES_BEFORE_RESTART = 5
MAX_RECOVERY_ATTEMPTS = 3

# Orchestration behavior.
ORCHESTRATION_WAIT_SECONDS = 10
