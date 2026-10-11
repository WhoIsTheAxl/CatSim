"""World and resource definitions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Place:
    name: str
    neighbors: tuple[str, ...]
    food: bool = False
    water: bool = False
    shelter: bool = False
    toy: bool = False


WORLD = {
    "Living Room": Place("Living Room", ("Kitchen", "Bedroom", "Cardboard Box"), toy=True),
    "Kitchen": Place("Kitchen", ("Living Room",), food=True, water=True),
    "Bedroom": Place("Bedroom", ("Living Room",), shelter=True),
    "Cardboard Box": Place("Cardboard Box", ("Living Room",), shelter=True),
}


