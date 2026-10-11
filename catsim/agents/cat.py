"""Cat agent: coordinates needs, perception, cognition and action execution."""
import random
from catsim.biology.needs import Needs
from catsim.biology.metabolism import Metabolism
from catsim.biology.activity_budget import ActivityBudget, apply_activity
from catsim.biology.clock import SimulationClock
from catsim.biology.personality import Personality
from catsim.behavior.regulation import Regulation
from catsim.simulation.metrics import Metrics
from catsim.behavior.arousal import should_interrupt_rest
from catsim.behavior.interruptions import should_interrupt_for_needs
from catsim.cognition.memory import Memory
from catsim.cognition.decision import DecisionSystem
from catsim.behavior.execution import BehaviorExecutor
from catsim.behavior.activity import Activity
from catsim.world.environment import Environment
from catsim.perception.sensory_system import SensorySystem


class Cat(DecisionSystem, BehaviorExecutor):
    def __init__(self, name: str = "Mochi", seed: int = 42,
                 world: Environment | None = None,
                 personality: Personality | None = None,
                 regulation: Regulation | None = None,
                 tick_minutes: float = 1.0,
                 metabolism: Metabolism | None = None):
        self.name = name
        self.personality = personality or Personality()
        self.regulation = regulation or Regulation()
        if tick_minutes <= 0:
            raise ValueError('tick_minutes must be positive')
        self.clock = SimulationClock(tick_minutes=tick_minutes)
        self.metabolism = metabolism or Metabolism()
        self.activity_budget = ActivityBudget()
        self.metrics = Metrics()
        self.rng = random.Random(seed)
        self.world = world if world is not None else Environment()
        self.senses = SensorySystem()
        self.location = "Living Room"
        self.needs = Needs()
        self.memory = Memory()
        self.observations = ()
        self.new_stimuli = ()
        self._noticed_sounds: set[str] = set()
        self.perceive()
        self.activity: Activity | None = None
        self.last_destination: str | None = None
        self.cooldowns: dict[str, int] = {}
        self.scores: dict[str, float] = {}
        self.final_scores: dict[str, float] = {}
        self.adjustments: dict[str, float] = {}
        self.goal = None
        self.navigation_target = None

    def perceive(self) -> None:
        self.observations = self.senses.observe(self.location, self.world)
        self.new_stimuli = tuple(item for item in self.observations
                                 if item.kind == 'sound' and item.object_id not in self._noticed_sounds)
        self.memory.observe(self.world.places[self.location], self.observations)
        for item in self.observations:
            if item.kind == "sound" and item.object_id not in self._noticed_sounds:
                self._noticed_sounds.add(item.object_id)
                self.needs.fear = min(100, self.needs.fear + item.intensity * 0.1)

    def step(self) -> str:
        self.clock.advance()
        self.needs.tick(self.clock.tick_minutes, self.metabolism)
        for action in list(self.cooldowns):
            self.cooldowns[action] -= self.clock.tick_minutes
            if self.cooldowns[action] <= 0:
                del self.cooldowns[action]
        self.perceive()
        if self.navigation_target == self.location:
            self.navigation_target = None
        disturbed = should_interrupt_rest(self.activity, self.new_stimuli)
        need_interruption = not disturbed and should_interrupt_for_needs(self)
        interrupted = disturbed or need_interruption
        if interrupted:
            self.activity = None
        if self.activity is None:
            self.activity = self.choose()
            event = (f"interrupts activity; starts {self.activity.name}"
                     if interrupted else f"starts {self.activity.name}")
        else:
            event = f"continues {self.activity.name}"
        apply_activity(self.needs, self.activity.name, self.clock.tick_minutes, self.activity_budget)
        self.activity.remaining -= 1
        if self.activity.remaining <= 0:
            event += f"; {self.finish(self.activity)}"
            self.activity = None
        self.metrics.record(event, self.location)
        return event
