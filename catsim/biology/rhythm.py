"""Experimental daily activity modulation.

Twilight activity peaks are research-informed; curve amplitude and timing
are illustrative, not fitted to observed cats.
"""
import math


def activity_drive(hour: float) -> float:
    """Return 0..1 activity propensity, with dawn/dusk peaks."""
    def peak(center: float) -> float:
        distance = min(abs(hour - center) % 24, 24 - abs(hour - center) % 24)
        return math.exp(-0.5 * (distance / 2.5) ** 2)
    return min(1.0, 0.25 + 0.55 * max(peak(6), peak(18)))


def rest_drive(hour: float) -> float:
    return 1.0 - activity_drive(hour)
