"""Research-informed, experimental cat behavior simulator."""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field


def clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


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


@dataclass
class Needs:
    hunger: float = 35.0
    thirst: float = 20.0
    fatigue: float = 25.0
    fear: float = 15.0
    curiosity: float = 60.0
    grooming_urge: float = 28.0
    play_urge: float = 45.0

    def tick(self) -> None:
        self.hunger = clamp(self.hunger + 0.8)
        self.thirst = clamp(self.thirst + 1.0)
        self.fatigue = clamp(self.fatigue + 0.5)
        self.fear = clamp(self.fear - 0.2)
        self.curiosity = clamp(self.curiosity + 0.2)
        self.grooming_urge = clamp(self.grooming_urge + 0.35)
        self.play_urge = clamp(self.play_urge + 0.4)


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


@dataclass
class Activity:
    name: str
    remaining: int
    destination: str | None = None


class Cat:
    def __init__(self, name: str = "Mochi", seed: int = 42):
        self.name = name
        self.rng = random.Random(seed)
        self.location = "Living Room"
        self.needs = Needs()
        self.memory = Memory()
        self.memory.observe(WORLD[self.location])
        self.activity: Activity | None = None
        self.last_destination: str | None = None
        self.cooldowns: dict[str, int] = {}
        self.scores: dict[str, float] = {}

    def utilities(self) -> dict[str, float]:
        n = self.needs
        place = WORLD[self.location]
        scores: dict[str, float] = {
            "rest": 8 + n.fatigue * 0.3,
            "sleep": n.fatigue * 1.2 + (18 if place.shelter else 0),
            "groom": n.grooming_urge * 0.7,
        }
        if place.food:
            scores["eat"] = n.hunger * 1.5
        if place.water:
            scores["drink"] = n.thirst * 1.6
        if place.toy:
            scores["play"] = n.play_urge * 0.9 - n.fatigue * 0.25
        if place.shelter:
            scores["hide"] = n.fear * 1.4

        for destination in place.neighbors:
            known = self.memory.resources.get(destination, set())
            familiarity = self.memory.familiarity.get(destination, 0)
            score = (
                n.curiosity * 0.45
                + (100 - familiarity) * 0.25
                - n.fear * 0.35
                - n.fatigue * 0.15
            )
            if "food" in known:
                score += n.hunger * 0.85
            if "water" in known:
                score += n.thirst * 0.85
            if "shelter" in known:
                score += n.fear * 0.6 + n.fatigue * 0.15
            if destination == self.last_destination:
                score -= 24
            scores["move:" + destination] = score

        for action, remaining in self.cooldowns.items():
            if remaining > 0:
                scores.pop(action, None)
        return scores

    def choose(self) -> Activity:
        self.scores = self.utilities()
        # Small seeded variation breaks ties without dominating motivation.
        action = max(self.scores, key=lambda a: self.scores[a] + self.rng.uniform(-2, 2))
        durations = {"sleep": 5, "groom": 2, "eat": 2, "drink": 2,
                     "play": 3, "hide": 3, "rest": 2}
        return Activity(action, durations.get(action, 2),
                        action.split(":", 1)[1] if action.startswith("move:") else None)

    def finish(self, activity: Activity) -> str:
        n = self.needs
        action = activity.name
        if action == "eat":
            n.hunger = clamp(n.hunger - 35)
        elif action == "drink":
            n.thirst = clamp(n.thirst - 40)
        elif action == "sleep":
            n.fatigue = clamp(n.fatigue - 36)
        elif action == "groom":
            n.grooming_urge = clamp(n.grooming_urge - 40)
        elif action == "play":
            n.play_urge = clamp(n.play_urge - 38)
            n.fatigue = clamp(n.fatigue + 7)
        elif action == "hide":
            n.fear = clamp(n.fear - 16)
        elif action == "rest":
            n.fatigue = clamp(n.fatigue - 7)
        elif action.startswith("move:"):
            origin = self.location
            self.location = activity.destination or origin
            self.last_destination = origin
            self.memory.observe(WORLD[self.location])
            n.curiosity = clamp(n.curiosity - 6)
            n.fatigue = clamp(n.fatigue + 2)
            return f"arrives at {self.location}"
        self.cooldowns[action] = {"groom": 10, "sleep": 4, "play": 5,
                                  "eat": 4, "drink": 4}.get(action, 2)
        return f"finishes {action}"

    def step(self) -> str:
        self.needs.tick()
        for action in list(self.cooldowns):
            self.cooldowns[action] -= 1
            if self.cooldowns[action] <= 0:
                del self.cooldowns[action]
        if self.activity is None:
            self.activity = self.choose()
            event = f"starts {self.activity.name}"
        else:
            event = f"continues {self.activity.name}"
        self.activity.remaining -= 1
        if self.activity.remaining <= 0:
            event += f"; {self.finish(self.activity)}"
            self.activity = None
        return event


def run(steps: int = 100, seed: int = 42, debug: bool = False) -> list[str]:
    cat = Cat(seed=seed)
    events = []
    for tick in range(1, steps + 1):
        event = cat.step()
        n = cat.needs
        line = (f"[T={tick:03}] {cat.name} {event} | {cat.location} "
                f"H={n.hunger:.1f} T={n.thirst:.1f} F={n.fatigue:.1f} "
                f"Fear={n.fear:.1f}")
        events.append(line)
        print(line)
        if debug and "starts " in event:
            print("  utilities:", ", ".join(
                f"{key}={value:.1f}" for key, value in
                sorted(cat.scores.items(), key=lambda item: -item[1])))
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description="CatSim experimental behavioral simulator")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.steps < 0:
        parser.error("--steps must be nonnegative")
    run(args.steps, args.seed, args.debug)


if __name__ == "__main__":
    main()
