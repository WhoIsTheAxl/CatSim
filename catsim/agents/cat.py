"""Cat agent: coordinates needs, perception, cognition and action execution."""
import random
from catsim.biology.needs import Needs
from catsim.cognition.memory import Memory
from catsim.cognition.decision import DecisionSystem
from catsim.behavior.execution import BehaviorExecutor
from catsim.behavior.activity import Activity
from catsim.world.environment import Environment
from catsim.perception.sensory_system import SensorySystem


class Cat(DecisionSystem, BehaviorExecutor):
    def __init__(self, name: str = "Mochi", seed: int = 42,
                 world: Environment | None = None):
        self.name = name
        self.rng = random.Random(seed)
        self.world = world if world is not None else Environment()
        self.senses = SensorySystem()
        self.location = "Living Room"
        self.needs = Needs()
        self.memory = Memory()
        self.observations = ()
        self.perceive()
        self.activity: Activity | None = None
        self.last_destination: str | None = None
        self.cooldowns: dict[str, int] = {}
        self.scores: dict[str, float] = {}
        self.goal = None

    def perceive(self) -> None:
        self.observations = self.senses.observe(self.location, self.world)
        self.memory.observe(self.world.places[self.location], self.observations)
        for item in self.observations:
            if item.kind == "sound":
                self.needs.fear = min(100, self.needs.fear + item.intensity * 0.1)

    def step(self) -> str:
        self.needs.tick()
        for action in list(self.cooldowns):
            self.cooldowns[action] -= 1
            if self.cooldowns[action] <= 0:
                del self.cooldowns[action]
        if self.activity is None:
            self.perceive()
            self.activity = self.choose()
            event = f"starts {self.activity.name}"
        else:
            event = f"continues {self.activity.name}"
        self.activity.remaining -= 1
        if self.activity.remaining <= 0:
            event += f"; {self.finish(self.activity)}"
            self.activity = None
        return event
