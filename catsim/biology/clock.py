"""Explicit simulation time. Tick length is a configurable model assumption."""
from dataclasses import dataclass


@dataclass
class SimulationClock:
    tick_minutes: float = 1.0
    ticks: int = 0

    def advance(self) -> None:
        if self.tick_minutes <= 0:
            raise ValueError("tick_minutes must be positive")
        self.ticks += 1

    @property
    def elapsed_minutes(self) -> float:
        return self.ticks * self.tick_minutes

    @property
    def hour_of_day(self) -> float:
        return (self.elapsed_minutes / 60) % 24
