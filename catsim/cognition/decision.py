"""Experimental utility-based choices, gated by behavioral eligibility."""
from catsim.behavior.activity import Activity
from catsim.behavior.navigation import next_step
from catsim.cognition.goals import Goal
from catsim.biology.rhythm import activity_drive, rest_drive
from catsim.behavior.resting import preferred_rest_site


class DecisionSystem:
    def utilities(self) -> dict[str, float]:
        n = self.needs
        place = self.world.places[self.location]
        perceived = {item.kind for item in self.observations}
        reg = self.regulation
        scores: dict[str, float] = {"idle": 9.0}
        rhythm = activity_drive(self.clock.hour_of_day)
        rest_rhythm = rest_drive(self.clock.hour_of_day)

        if reg.eligible("rest", n):
            scores["rest"] = 8 + n.fatigue * 0.3
        if reg.eligible("sleep", n):
            scores["sleep"] = n.fatigue * (0.9 + rest_rhythm * 0.5) + (24 if "shelter" in perceived else -12)
        if reg.eligible("groom", n):
            scores["groom"] = n.grooming_urge * 0.7
        if "food" in perceived and reg.eligible("eat", n):
            scores["eat"] = n.hunger * 1.5
        if "water" in perceived and reg.eligible("drink", n):
            scores["drink"] = n.thirst * 1.6
        if "toy" in perceived and reg.eligible("play", n):
            scores["play"] = n.play_urge * self.personality.playfulness * (1.2 + rhythm * 0.5) - n.fatigue * 0.25
        if "shelter" in perceived and reg.eligible("hide", n):
            scores["hide"] = n.fear * 1.4
        if "novel_object" in perceived and reg.eligible("investigate", n):
            scores["investigate"] = n.curiosity * self.personality.curiosity - n.fear * 0.3

        for destination in place.neighbors:
            familiarity = self.memory.familiarity.get(destination, 0)
            novelty = (100 - familiarity) * 0.25
            score = (reg.exploration_floor + n.curiosity * self.personality.curiosity * 0.5
                     + novelty - n.fear * (1 - self.personality.boldness) * 0.5
                     - n.fatigue * 0.15)
            if destination == self.last_destination:
                score -= 12
            scores["move:" + destination] = score

        # Rest-site preference is informed by observed, remembered shelter.
        if reg.eligible("sleep", n):
            target = preferred_rest_site(self)
            if target is not None and target != self.location:
                step = next_step(self.world.places, self.location, target)
                if step is not None:
                    key = "move:" + step
                    scores[key] = max(scores.get(key, 0), n.fatigue * (0.9 + rest_rhythm * 0.5) + 15)

        # Navigation uses remembered observations, not omniscient world objects.
        for destination, kinds in self.memory.resources.items():
            if destination == self.location:
                continue
            step = next_step(self.world.places, self.location, destination)
            if step is None:
                continue
            motivation = 0.0
            if "food" in kinds and reg.eligible("eat", n):
                motivation = max(motivation, n.hunger * 1.3)
            if "water" in kinds and reg.eligible("drink", n):
                motivation = max(motivation, n.thirst * 1.4)
            if "shelter" in kinds and reg.eligible("hide", n):
                motivation = max(motivation, n.fear * 0.9)
            if "shelter" in kinds and reg.eligible("sleep", n):
                motivation = max(motivation, n.fatigue * 0.9)
            key = "move:" + step
            if motivation:
                scores[key] = max(scores.get(key, 0), motivation)

        for action in self.cooldowns:
            scores.pop(action, None)
        return scores

    def choose(self) -> Activity:
        self.scores = self.utilities()
        self.adjustments = {action: self.rng.uniform(-2, 2) for action in self.scores}
        self.final_scores = {
            action: value + self.adjustments[action]
            for action, value in self.scores.items()
        }
        action = max(self.final_scores, key=self.final_scores.get)
        self.goal = (Goal("navigate", action.split(":", 1)[1], self.scores[action])
                     if action.startswith("move:") else
                     Goal(action, self.location, self.scores[action]))
        durations = {"sleep": 5, "groom": 2, "eat": 2, "drink": 2,
                     "play": 3, "hide": 3, "rest": 2, "investigate": 3, "idle": 2}
        return Activity(action, durations.get(action, 2),
                        action.split(":", 1)[1] if action.startswith("move:") else None)
