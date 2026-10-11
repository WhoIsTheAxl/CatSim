"""Experimental eligibility thresholds and utility shaping.

These numbers are simulation hypotheses, NOT measured feline thresholds.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Regulation:
    eat_start: float = 28.0
    drink_start: float = 25.0
    sleep_start: float = 32.0
    rest_start: float = 18.0
    groom_start: float = 22.0
    play_start: float = 25.0
    hide_start: float = 20.0
    investigate_start: float = 25.0
    # Allow curiosity-driven wandering without making movement mandatory.
    exploration_floor: float = 8.0

    def eligible(self, action: str, needs) -> bool:
        thresholds = {
            "eat": (needs.hunger, self.eat_start),
            "drink": (needs.thirst, self.drink_start),
            "sleep": (needs.fatigue, self.sleep_start),
            "rest": (needs.fatigue, self.rest_start),
            "groom": (needs.grooming_urge, self.groom_start),
            "play": (needs.play_urge, self.play_start),
            "hide": (needs.fear, self.hide_start),
            "investigate": (needs.curiosity, self.investigate_start),
        }
        return action not in thresholds or thresholds[action][0] >= thresholds[action][1]
