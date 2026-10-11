"""Immutable observations: what a cat senses, not what exists everywhere."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    object_id: str
    kind: str
    location: str
    intensity: float = 0.0
