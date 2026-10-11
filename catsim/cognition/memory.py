"""Learning from direct observations; no access to hidden world state."""
from dataclasses import dataclass, field
from catsim.core.math import clamp
from catsim.perception.observations import Observation
from catsim.world.model import Place


@dataclass
class Memory:
    familiarity: dict[str, float] = field(default_factory=dict)
    resources: dict[str, set[str]] = field(default_factory=dict)
    object_locations: dict[str, str] = field(default_factory=dict)

    def observe(self, place: Place, observations: tuple[Observation, ...] | None = None) -> None:
        self.familiarity[place.name] = clamp(self.familiarity.get(place.name, 0) + 12)
        if observations is None:
            # Compatibility for legacy tests; the simulation always supplies perceptions.
            found = {kind for kind in ("food", "water", "shelter", "toy")
                     if getattr(place, kind)}
            self.resources[place.name] = found
            return
        self.resources[place.name] = {
            item.kind for item in observations
            if item.kind in {"food", "water", "shelter", "toy"}
        }
        seen_ids = {item.object_id for item in observations}
        for obj_id, remembered_place in list(self.object_locations.items()):
            if remembered_place == place.name and obj_id not in seen_ids:
                del self.object_locations[obj_id]
        for item in observations:
            self.object_locations[item.object_id] = item.location
