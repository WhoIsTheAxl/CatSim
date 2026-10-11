"""Observation-based utility choices and need-directed resource discovery.

Utilities are hypotheses, not empirical feline behavior probabilities.
Unknown resources cannot be selected by consulting world objects.
"""
import math
from catsim.behavior.activity import Activity
from catsim.behavior.navigation import next_step
from catsim.cognition.goals import Goal
from catsim.biology.rhythm import activity_drive, rest_drive
from catsim.behavior.resting import preferred_rest_site


class DecisionSystem:
    def utilities(self) -> dict[str, float]:
        n, reg = self.needs, self.regulation
        perceived = {item.kind for item in self.observations}
        scores = {"idle": 14.0}
        rhythm = activity_drive(self.clock.hour_of_day)
        rest_rhythm = rest_drive(self.clock.hour_of_day)
        if reg.eligible("rest", n):
            scores["rest"] = 7 + n.fatigue * .35 + (7 if "shelter" in perceived else 0)
        if reg.eligible("sleep", n):
            scores["sleep"] = n.fatigue * (.9 + rest_rhythm * .5) + (24 if "shelter" in perceived else -20)
        if reg.eligible("groom", n):
            scores["groom"] = n.grooming_urge * .7
        if "food" in perceived and reg.eligible("eat", n):
            scores["eat"] = n.hunger * 1.5
        if "water" in perceived and reg.eligible("drink", n):
            scores["drink"] = n.thirst * 1.6
        if "toy" in perceived and reg.eligible("play", n):
            scores["play"] = (n.play_urge * self.personality.playfulness * (1.2 + rhythm * .5)
                              * self.play_habituation.play_multiplier - n.fatigue * .25)
        if "shelter" in perceived and reg.eligible("hide", n):
            scores["hide"] = n.fear * 1.4
        if "novel_object" in perceived and reg.eligible("investigate", n):
            scores["investigate"] = n.curiosity * self.personality.curiosity - n.fear * .3

        known_food = any("food" in kinds for kinds in self.memory.resources.values())
        known_water = any("water" in kinds for kinds in self.memory.resources.values())
        # Missing resources produce search motivation, NOT knowledge of their position.
        unmet_search = max(
            n.hunger * .95 if reg.eligible("eat", n) and not known_food else 0,
            n.thirst * 1.15 if reg.eligible("drink", n) and not known_water else 0,
        )
        for destination in self.world.places[self.location].neighbors:
            familiarity = self.memory.familiarity.get(destination, 0)
            novelty = (100 - familiarity) * .16 * (n.curiosity / 100)
            score = (n.curiosity * self.personality.curiosity * .24 + novelty
                     - n.fear * (1 - self.personality.boldness) * .5
                     - n.fatigue * .15)
            if destination == self.last_destination:
                score -= 12
            # Prefer less familiar reachable rooms when searching for unknown necessities.
            search_score = unmet_search + (100 - familiarity) * .12
            if destination == self.last_destination:
                search_score -= 8
            score = max(score, search_score if unmet_search else score)
            if score > 0:
                scores["move:" + destination] = score

        # Leave resource-only rooms once feeding and drinking needs are met.
        # Use only observed resources and remembered neighboring enrichment.
        if (("food" in perceived or "water" in perceived)
                and "toy" not in perceived and "shelter" not in perceived
                and not reg.eligible("eat", n) and not reg.eligible("drink", n)):
            for destination in self.world.places[self.location].neighbors:
                known = self.memory.resources.get(destination, set())
                if "toy" in known or "shelter" in known:
                    key = "move:" + destination
                    scores[key] = max(scores.get(key, 0), 21.0)

        if reg.eligible("sleep", n):
            target = preferred_rest_site(self)
            if target and target != self.location:
                step = next_step(self.world.places, self.location, target)
                if step:
                    key = "move:" + step
                    scores[key] = max(scores.get(key, 0), n.fatigue * (.9 + rest_rhythm * .5) + 15)

        for destination, kinds in self.memory.resources.items():
            if destination == self.location:
                continue
            step = next_step(self.world.places, self.location, destination)
            if not step:
                continue
            motivation = max(
                n.hunger * 1.35 if "food" in kinds and reg.eligible("eat", n) else 0,
                n.thirst * 1.45 if "water" in kinds and reg.eligible("drink", n) else 0,
                n.fear * .9 if "shelter" in kinds and reg.eligible("hide", n) else 0,
                n.fatigue * .9 if "shelter" in kinds and reg.eligible("sleep", n) else 0,
            )
            if motivation:
                key = "move:" + step
                scores[key] = max(scores.get(key, 0), motivation)

        # Existing intentions only affect legal adjacent steps; local urgent
        # actions are still free to compete rather than being overridden later.
        target = self.navigation_target
        if target and target != self.location:
            step = next_step(self.world.places, self.location, target)
            if step:
                key = "move:" + step
                scores[key] = max(scores.get(key, 0), 35.0)
        for action in self.cooldowns:
            if action != "idle":
                scores.pop(action, None)
        return scores

    def choose(self) -> Activity:
        self.scores = self.utilities()
        self.adjustments = {key: self.rng.uniform(-2, 2) for key in self.scores}
        self.final_scores = {key: score + self.adjustments[key]
                             for key, score in self.scores.items()}
        action = max(self.final_scores, key=self.final_scores.get)
        if action.startswith("move:"):
            step = action.split(":", 1)[1]
            if self.navigation_target is None:
                candidates = []
                for destination, kinds in self.memory.resources.items():
                    if destination == self.location or next_step(
                            self.world.places, self.location, destination) != step:
                        continue
                    urgency = max(
                        self.needs.hunger * 1.35 if "food" in kinds and self.regulation.eligible("eat", self.needs) else 0,
                        self.needs.thirst * 1.45 if "water" in kinds and self.regulation.eligible("drink", self.needs) else 0,
                        self.needs.fatigue if "shelter" in kinds and self.regulation.eligible("sleep", self.needs) else 0,
                    )
                    if urgency:
                        candidates.append((urgency, destination))
                if candidates:
                    self.navigation_target = max(candidates)[1]
        self.goal = (Goal("navigate", action.split(":", 1)[1], self.scores[action])
                     if action.startswith("move:") else
                     Goal(action, self.location, self.scores[action]))
        durations_minutes = {"sleep": 60, "groom": 6, "eat": 10, "drink": 3,
                             "play": 12, "hide": 15, "rest": 20,
                             "investigate": 5, "idle": 15, "move": 3}
        kind = "move" if action.startswith("move:") else action
        duration = max(1, math.ceil(durations_minutes.get(kind, 10) / self.clock.tick_minutes))
        return Activity(action, duration,
                        action.split(":", 1)[1] if action.startswith("move:") else None)
