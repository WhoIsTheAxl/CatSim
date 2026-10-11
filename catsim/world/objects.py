"""Physical resources and stimuli, independent of room definitions."""
from dataclasses import dataclass


@dataclass
class WorldObject:
    id: str
    kind: str
    location: str
    visible: bool = True
    intensity: float = 0.0


def default_objects() -> dict[str, WorldObject]:
    return {
        "bowl_food": WorldObject("bowl_food", "food", "Kitchen"),
        "bowl_water": WorldObject("bowl_water", "water", "Kitchen"),
        "bed": WorldObject("bed", "shelter", "Bedroom"),
        "box": WorldObject("box", "shelter", "Cardboard Box"),
        "mouse_toy": WorldObject("mouse_toy", "toy", "Living Room"),
    }
