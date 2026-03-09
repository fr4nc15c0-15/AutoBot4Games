"""Monitor power control utilities.

This module attempts to turn off monitor while leaving automation active.
"""

from __future__ import annotations

import platform
import subprocess

from utils.logger import get_logger

LOGGER = get_logger(__name__)


def turn_off_monitor() -> bool:
    """Turn off monitor depending on OS support and return success state."""
    system = platform.system().lower()
    try:
        if "windows" in system:
            # Uses PowerShell command to request monitor sleep without ending the process.
            command = (
                "(Add-Type '[DllImport(\"user32.dll\")]public static extern int "
                "SendMessage(int hWnd,int hMsg,int wParam,int lParam);' -Name a -Pas)::"
                "SendMessage(-1,0x0112,0xF170,2)"
            )
            subprocess.run(["powershell", command], check=False)
            return True
        if "linux" in system:
            subprocess.run(["xset", "dpms", "force", "off"], check=False)
            return True
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Failed to turn off monitor: %s", exc)
    return False
