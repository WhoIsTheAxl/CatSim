"""Environmental changes are injected explicitly for reproducible experiments."""
from dataclasses import dataclass
from catsim.world.environment import Environment
from catsim.world.objects import WorldObject


@dataclass(frozen=True)
class Event:
    kind: str
    location: str
    intensity: float = 50.0
    identifier: str = "stimulus"


def apply_event(world: Environment, event: Event) -> None:
    if event.kind not in {"sound", "novel_object"}:
        raise ValueError(f"Unsupported event: {event.kind}")
    world.add_object(WorldObject(event.identifier, event.kind, event.location,
                                 intensity=event.intensity))
