"""Global runtime settings for the automation framework.

This file centralizes all constants controlling timing, retries, confidence,
thread intervals, and recovery thresholds.
"""

from __future__ import annotations

# --- PyAutoGUI safety and baseline behavior ---------------------------------
PYAUTOGUI_PAUSE = 0.05
FAILSAFE_ENABLED = True

# --- Vision defaults ---------------------------------------------------------
DEFAULT_TEMPLATE_CONFIDENCE = 0.86
DEFAULT_TIMEOUT_SECONDS = 5.0
DEFAULT_RETRY_COUNT = 3
DEFAULT_RETRY_DELAY = 0.4

# --- OCR defaults ------------------------------------------------------------
OCR_PSM_MODE = 7
OCR_LANG = "eng"

# --- Human-like mouse/keyboard behavior -------------------------------------
MOUSE_OFFSET_PIXELS = 6
MOUSE_MIN_DURATION = 0.08
MOUSE_MAX_DURATION = 0.20
ACTION_DELAY_MIN = 0.05
ACTION_DELAY_MAX = 0.20

# --- Background thread intervals --------------------------------------------
POPUP_SCAN_INTERVAL = 1.0
WATCHDOG_INTERVAL = 2.0
SCHEDULER_INTERVAL = 0.5

# --- Recovery policy ---------------------------------------------------------
FREEZE_TIMEOUT_SECONDS = 45.0
MAX_UI_FAILURES_BEFORE_RECOVERY = 3
MAX_RECOVERY_ATTEMPTS = 3

# --- Master orchestration ----------------------------------------------------
ORCHESTRATION_WAIT_SECONDS = 10
GAME_STARTUP_WAIT_SECONDS = 12
