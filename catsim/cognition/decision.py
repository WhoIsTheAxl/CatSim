from catsim.behavior.activity import Activity
from catsim.world.model import WORLD

class DecisionSystem:
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

