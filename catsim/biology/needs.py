"""Experimental internal-state dynamics."""
from dataclasses import dataclass
from catsim.core.math import clamp
from catsim.biology.metabolism import Metabolism

@dataclass
class Needs:
    hunger: float = 35.0
    thirst: float = 20.0
    fatigue: float = 25.0
    fear: float = 15.0
    curiosity: float = 60.0
    grooming_urge: float = 28.0
    play_urge: float = 45.0

    def tick(self, minutes: float = 1.0, metabolism: Metabolism | None = None) -> None:
        if minutes < 0:
            raise ValueError('minutes must be nonnegative')
        rates = metabolism or Metabolism()
        hours = minutes / 60
        self.hunger = clamp(self.hunger + rates.hunger_per_hour * hours)
        self.thirst = clamp(self.thirst + rates.thirst_per_hour * hours)
        self.fatigue = clamp(self.fatigue + rates.fatigue_per_hour * hours)
        self.fear = clamp(self.fear - rates.fear_recovery_per_hour * hours)
        self.curiosity = clamp(self.curiosity + rates.curiosity_per_hour * hours)
        self.grooming_urge = clamp(self.grooming_urge + rates.grooming_per_hour * hours)
        self.play_urge = clamp(self.play_urge + rates.play_per_hour * hours)


