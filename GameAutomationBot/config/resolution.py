"""Resolution profile configuration.

Profiles provide a normalized place to keep monitor presets and scaling factors
for users running automation at different resolutions.
"""

from __future__ import annotations

SUPPORTED_RESOLUTIONS = {
    "1080p": {"width": 1920, "height": 1080, "scale": 1.0},
    "1440p": {"width": 2560, "height": 1440, "scale": 1.3333},
    "4k": {"width": 3840, "height": 2160, "scale": 2.0},
}

DEFAULT_PROFILE = "1080p"
