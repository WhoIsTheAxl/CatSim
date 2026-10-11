"""Mutable world container; cat cognition does not access hidden objects."""
from dataclasses import dataclass, field
from catsim.world.model import WORLD, Place
from catsim.world.objects import WorldObject, default_objects


@dataclass
class Environment:
    places: dict[str, Place] = field(default_factory=lambda: dict(WORLD))
    objects: dict[str, WorldObject] = field(default_factory=default_objects)

    def move_object(self, object_id: str, location: str) -> None:
        if location not in self.places:
            raise ValueError(f"Unknown location: {location}")
        self.objects[object_id].location = location

    def add_object(self, obj: WorldObject) -> None:
        if obj.location not in self.places:
            raise ValueError(f"Unknown location: {obj.location}")
        self.objects[obj.id] = obj
