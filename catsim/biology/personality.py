"""Individual behavioral variation; coefficients are experimental."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Personality:
    boldness: float = 0.5
    curiosity: float = 0.7
    playfulness: float = 0.6

    def __post_init__(self) -> None:
        for value in (self.boldness, self.curiosity, self.playfulness):
            if not 0 <= value <= 1:
                raise ValueError("Personality traits must be between 0 and 1")
