"""Experimental internal-state dynamics."""
from dataclasses import dataclass
from catsim.core.math import clamp

@dataclass
class Needs:
    hunger: float = 35.0
    thirst: float = 20.0
    fatigue: float = 25.0
    fear: float = 15.0
    curiosity: float = 60.0
    grooming_urge: float = 28.0
    play_urge: float = 45.0

    def tick(self) -> None:
        self.hunger = clamp(self.hunger + 0.8)
        self.thirst = clamp(self.thirst + 1.0)
        self.fatigue = clamp(self.fatigue + 0.5)
        self.fear = clamp(self.fear - 0.2)
        self.curiosity = clamp(self.curiosity + 0.2)
        self.grooming_urge = clamp(self.grooming_urge + 0.35)
        self.play_urge = clamp(self.play_urge + 0.4)


