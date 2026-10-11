"""Experimental, time-scaled habituation to repeated object play.

Inspired by Hall, Bradshaw & Robinson (2002), DOI:
10.1016/S0168-1591(02)00153-3. Their study supports rapid habituation
and recovery with stimulus changes; the numerical rates here are hypotheses.
"""
from dataclasses import dataclass
from catsim.core.math import clamp


@dataclass
class PlayHabituation:
    familiarity: float = 0.0
    gain_per_play_hour: float = 35.0
    recovery_per_nonplay_hour: float = 9.0

    def advance(self, activity: str, minutes: float) -> None:
        if minutes < 0:
            raise ValueError("minutes must be nonnegative")
        rate = (self.gain_per_play_hour if activity == "play"
                else -self.recovery_per_nonplay_hour)
        self.familiarity = clamp(self.familiarity + rate * minutes / 60.0)

    @property
    def play_multiplier(self) -> float:
        # Does not remove the underlying need to play; only reduces interest
        # in the same unchanging toy.
        return max(0.25, 1.0 - 0.012 * self.familiarity)

    def novel_toy(self) -> None:
        """Call when the toy's sensory characteristics change."""
        self.familiarity = 0.0
