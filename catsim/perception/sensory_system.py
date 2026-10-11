"""Local perception model; range and modality are experimental."""
from catsim.perception.observations import Observation
from catsim.world.environment import Environment


class SensorySystem:
    def observe(self, location: str, world: Environment) -> tuple[Observation, ...]:
        return tuple(
            Observation(obj.id, obj.kind, obj.location, obj.intensity)
            for obj in world.objects.values()
            if obj.location == location and obj.visible
        )
