"""Apply completed behaviors to cat state and world knowledge."""
from catsim.core.math import clamp
from catsim.behavior.activity import Activity


class BehaviorExecutor:
    def finish(self, activity: Activity) -> str:
        n = self.needs
        action = activity.name
        if action.startswith("move:"):
            origin = self.location
            self.location = activity.destination or origin
            self.last_destination = origin
            self.perceive()
            return f"arrives at {self.location}"
        if action not in {"idle", "rest"}:
            self.cooldowns[action] = {"groom": 10, "sleep": 20, "play": 10,
                                      "eat": 15, "drink": 10, "investigate": 10}.get(action, 3)
        return f"finishes {action}"
