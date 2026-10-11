from catsim.core.math import clamp
from catsim.world.model import WORLD
from catsim.behavior.activity import Activity

class BehaviorExecutor:
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

