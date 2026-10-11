from dataclasses import dataclass, field
from catsim.core.math import clamp
from catsim.world.model import Place

@dataclass
class Memory:
    familiarity: dict[str, float] = field(default_factory=dict)
    resources: dict[str, set[str]] = field(default_factory=dict)

    def observe(self, place: Place) -> None:
        self.familiarity[place.name] = clamp(self.familiarity.get(place.name, 0) + 12)
        found = set()
        for name in ("food", "water", "shelter", "toy"):
            if getattr(place, name):
                found.add(name)
        self.resources[place.name] = found


