import random
from catsim.biology.needs import Needs
from catsim.cognition.memory import Memory
from catsim.cognition.decision import DecisionSystem
from catsim.behavior.execution import BehaviorExecutor
from catsim.behavior.activity import Activity
from catsim.world.model import WORLD

class Cat(DecisionSystem, BehaviorExecutor):
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


