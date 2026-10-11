"""Activity frequencies and room occupancy for experiments."""
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Metrics:
    actions: Counter = field(default_factory=Counter)
    locations: Counter = field(default_factory=Counter)
    ticks: int = 0

    def record(self, event: str, location: str) -> None:
        self.ticks += 1
        self.locations[location] += 1
        if event.startswith("starts "):
            self.actions[event.split("starts ", 1)[1].split(";", 1)[0]] += 1

    def report(self) -> dict:
        return {"ticks": self.ticks, "actions": dict(self.actions),
                "locations": dict(self.locations)}
