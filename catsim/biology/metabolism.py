"""Configurable time-normalized internal state rates (experimental units/hour)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Metabolism:
    hunger_per_hour: float = 2.0
    thirst_per_hour: float = 2.5
    fatigue_per_hour: float = 1.4
    fear_recovery_per_hour: float = 1.0
    curiosity_per_hour: float = 1.0
    grooming_per_hour: float = 1.1
    play_per_hour: float = 1.4

    def __post_init__(self):
        if any(value < 0 for value in vars(self).values()):
            raise ValueError("Metabolic rates must be nonnegative")
