"""Utility scoring with perceived resources and remembered navigation goals."""
from catsim.behavior.activity import Activity
from catsim.behavior.navigation import next_step
from catsim.cognition.goals import Goal


class DecisionSystem:
    def utilities(self) -> dict[str, float]:
        n = self.needs
        place = self.world.places[self.location]
        perceived = {item.kind for item in self.observations}
        scores: dict[str, float] = {
            "rest": 8 + n.fatigue * 0.3,
            "sleep": n.fatigue * 1.2 + (18 if "shelter" in perceived else 0),
            "groom": n.grooming_urge * 0.7,
        }
        if "food" in perceived:
            scores["eat"] = n.hunger * 1.5
        if "water" in perceived:
            scores["drink"] = n.thirst * 1.6
        if "toy" in perceived:
            scores["play"] = n.play_urge * 0.9 - n.fatigue * 0.25
        if "shelter" in perceived:
            scores["hide"] = n.fear * 1.4
        if "novel_object" in perceived:
            scores["investigate"] = n.curiosity * 0.65 - n.fear * 0.3

        for destination in place.neighbors:
            familiarity = self.memory.familiarity.get(destination, 0)
            score = (n.curiosity * 0.45 + (100 - familiarity) * 0.25
                     - n.fear * 0.35 - n.fatigue * 0.15)
            if destination == self.last_destination:
                score -= 24
            scores["move:" + destination] = score

        # Use learned resource locations, not world-wide omniscient queries.
        for destination, kinds in self.memory.resources.items():
            if destination == self.location:
                continue
            step = next_step(self.world.places, self.location, destination)
            if step is None:
                continue
            motivation = 0.0
            if "food" in kinds:
                motivation = max(motivation, n.hunger * 1.3)
            if "water" in kinds:
                motivation = max(motivation, n.thirst * 1.4)
            if "shelter" in kinds:
                motivation = max(motivation, n.fear * 0.9 + n.fatigue * 0.25)
            key = "move:" + step
            scores[key] = max(scores.get(key, 0), motivation)

        for action in self.cooldowns:
            scores.pop(action, None)
        return scores

    def choose(self) -> Activity:
        self.scores = self.utilities()
        action = max(self.scores, key=lambda a: self.scores[a] + self.rng.uniform(-2, 2))
        self.goal = Goal("navigate", action.split(":", 1)[1], self.scores[action]) if action.startswith("move:") else Goal(action, self.location, self.scores[action])
        durations = {"sleep": 5, "groom": 2, "eat": 2, "drink": 2,
                     "play": 3, "hide": 3, "rest": 2, "investigate": 3}
        return Activity(action, durations.get(action, 2),
                        action.split(":", 1)[1] if action.startswith("move:") else None)
