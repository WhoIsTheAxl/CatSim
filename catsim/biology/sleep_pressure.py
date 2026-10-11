"""Experimental homeostatic sleep pressure, separate from fatigue.

The two-process sleep framework motivates the architecture, but the rates
and thresholds below are not fitted to domestic-cat sleep recordings.
"""
from dataclasses import dataclass
from catsim.core.math import clamp


@dataclass
class SleepPressure:
    value: float = 12.0
    wake_gain_per_hour: float = 4.0
    sleep_relief_per_hour: float = 12.0

    def advance(self, activity: str, minutes: float) -> None:
        if minutes < 0:
            raise ValueError("minutes must be nonnegative")
        rate = (-self.sleep_relief_per_hour if activity == "sleep"
                else self.wake_gain_per_hour)
        self.value = clamp(self.value + rate * minutes / 60.0)
