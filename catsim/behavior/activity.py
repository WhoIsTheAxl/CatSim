from dataclasses import dataclass

@dataclass
class Activity:
    name: str
    remaining: int
    destination: str | None = None


