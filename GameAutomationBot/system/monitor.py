"""Monitor power control utility.

Provides a best-effort implementation to turn off monitor while keeping
background automation logic active.
"""

from __future__ import annotations

import platform
import subprocess

from utils.logger import get_logger

LOGGER = get_logger(__name__)


def turn_off_monitor() -> bool:
    """Attempt to turn off display power based on active OS.

    Returns:
        True if command was issued successfully, otherwise False.
    """
    os_name = platform.system().lower()

    try:
        if "windows" in os_name:
            # Windows monitor-off message via PowerShell + user32 SendMessage.
            command = (
                "(Add-Type '[DllImport(\"user32.dll\")]public static extern int "
                "SendMessage(int hWnd,int hMsg,int wParam,int lParam);' -Name a -Pas)::"
                "SendMessage(-1,0x0112,0xF170,2)"
            )
            subprocess.run(["powershell", "-Command", command], check=False)
            return True

        if "linux" in os_name:
            # Linux DPMS off command. Requires X11 with xset support.
            subprocess.run(["xset", "dpms", "force", "off"], check=False)
            return True

        LOGGER.warning("Monitor off not implemented for OS: %s", os_name)
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Monitor-off command failed: %s", exc)

    return False
