"""Persistent high-level intentions with interruptible action selection."""
from dataclasses import dataclass


@dataclass
class Goal:
    kind: str
    target: str
    priority: float = 0.0
